from datetime import datetime
import json
from typing import List
import uuid
from pydantic import BaseModel, Field
from app.core.config import settings
from app.services.label import LabelService
from transformers import pipeline
from PIL import Image
from app.core.error import AppError
import paho.mqtt.client as mqtt
import cv2
import threading

class InferenceService:
    __IS_USE_LABELED_DATA_ONLY = True
    __CLASSIFY_INTERVAL = 2 # 2 seconds

    def __init__(self):
        self.image_classifier = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32", cache_dir="cache")  # Hugging Face model
        self.stop_events = {}  # store stop event. key: uri
        self.running_threads = {} # store running thread object. key: uri
        self.thread_info = {} # store thread infomation. key: pipeline_id
        self.pipeline_id_to_uri = {} # mapping pipeline_id to uri. key: pipeline_id, value: uri
        self.uri_to_pipeline_id = {} # mapping uri to pipeline_id. key: uri, value: pipeline_id
        self.pipeline_sequential_id = 1 # pipeline_id
        
    def start_pipeline(self, input: 'InferenceService.ClassifyStreamingInputDto'):
        if input.uri:
            if input.uri in self.running_threads: 
                raise AppError(message=f"{input.uri} already in progress")        
            else:
                event = threading.Event()
                self.stop_events[input.uri] = event
                task_thread = threading.Thread(target=self.__classify_streaming_task, args=(event, input))
                self.running_threads[input.uri] = task_thread
                self.pipeline_id_to_uri[self.pipeline_sequential_id] = input.uri
                self.uri_to_pipeline_id[input.uri] = self.pipeline_sequential_id
                self.__put_thread_info(input)
                self.pipeline_sequential_id += 1
                task_thread.start()                
        else:
            raise AppError(message="URI field not found in the input JSON data")
        
    def stop_pipeline(self, instance_id: int):
        uri = self.pipeline_id_to_uri.get(instance_id)
        if uri:
            event = self.stop_events.get(uri)
            if event:
                event.set()
                running_thread = self.running_threads.get(uri)
                if running_thread:
                    running_thread.join(10)
                    if not running_thread.is_alive():
                        del self.running_threads[uri]
                        del self.stop_events[uri]
            else:
                raise AppError(message=f"{uri} not in progress")
        else:
            raise AppError(message="URI field not found in the input JSON data")
        
    def get_pipelines(self) -> List['InferenceService.GetPipelinesOutputDto']:
        result = []
        for info in self.thread_info.values():
            result.append(InferenceService.GetPipelinesOutputDto(**info))
        
        return result
    
    def get_uri_by_pipeline_id(self, pipeline_id: int) -> str:
        return self.pipeline_id_to_uri.get(pipeline_id)

    def __classify_streaming_task(self, stop_event, input: 'InferenceService.ClassifyStreamingInputDto'):
        result_list = []
        mqtt_client = None
        pipeline_id = self.uri_to_pipeline_id[input.uri]

        # Open the RTSP stream using FFmpeg
        video = cv2.VideoCapture(input.uri, cv2.CAP_FFMPEG)
        if not video.isOpened():            
            print("Error opening video stream.")
            self.__set_thread_info_message(pipeline_id, "Error opening video stream.") 
            raise AppError(message="Error opening video stream.")
        
        avg_fps = video.get(cv2.CAP_PROP_FPS)
        self.thread_info[pipeline_id]['avg_fps'] = avg_fps
        fps = round(avg_fps)        
        
        if self.__is_need_to_connect_mqtt(input.mqtt_host):
            try:
                mqtt_client = self.__get_mqtt_client(input.mqtt_host, input.mqtt_topic)   
            except Exception as e:
                self.__set_thread_info_message(pipeline_id, str(e))   
                raise e

        label_service = LabelService()
        label_data = label_service.get_labels_by_uri(input.uri)
        if self.__IS_USE_LABELED_DATA_ONLY:
            if(len(label_data) == 0):
                self.__set_thread_info_message(pipeline_id, "No labeled data found. Need to label first.")
                raise AppError(message="No labeled data found. Need to label first.")
            
        frame_count = 0
        try:
            while not stop_event.is_set():
                ret, frame = video.read()
                if not ret:
                    print("Error reading frame from video stream.")
                    self.__set_thread_info_message(pipeline_id, "Error reading frame from video stream.")
                    raise AppError(message="Error reading frame from video stream.")
                
                frame_count += 1

                if frame_count % (self.__CLASSIFY_INTERVAL * fps) == 0:
                    # classify main frame
                    if not self.__IS_USE_LABELED_DATA_ONLY:
                        result_label, result_score = self.__classify_frame(frame)
                        result_list.append(input.device_name, result_label, result_score)

                    # classify labeled frames
                    result_list.extend(self.__classify_labeled_frames(frame, label_data))

                    if settings.DEBUG:
                        for result in result_list:
                            print(result)

                    # publish result
                    if self.__is_need_to_connect_mqtt(input.mqtt_host):                        
                        for result in result_list:
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Remove the last 3 characters
                            payload = {
                                "device_name": result[0],
                                "label": result[1],
                                "score": result[2],
                                "Timestamp": timestamp
                            }   
                            mqtt_client.publish(input.mqtt_topic, json.dumps(payload))
            self.thread_info[pipeline_id]['state'] = "COMPLETED"
        except Exception as e:
            self.__set_thread_info_message(pipeline_id, str(e))
            raise e
        finally:
            # 释放资源
            video.release()  
            if mqtt_client is not None and mqtt_client.is_connected():
                mqtt_client.disconnect()  
                mqtt_client = None

    def __classify_frame(self, frame):
        image_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        result_label, result_score = self.__classify_image(image_pil)
        return result_label, result_score

    def __classify_labeled_frames(self, frame, label_data):
        result = []
        for label in label_data:
            cropped_frame = frame[label.y1:label.y2, label.x1:label.x2]

            if settings.DEBUG:
                random_uuid = uuid.uuid4()
                image_name = f"output_images/frame_{random_uuid}_{label.equipment_no}.jpg"
                cv2.imwrite(image_name, cropped_frame)

            result_label, result_score = self.__classify_frame(cropped_frame)
            result.append((label.equipment_no, result_label, result_score))
        
        return result

    def __classify_image(self, image: Image):
        # 使用 Hugging Face model 進行預測
        outputs = self.image_classifier(image, candidate_labels=["green", "red", "yellow", "blue", "none"])
        result_label, result_score = self.__get_label_and_score_with_max_score(outputs)

        return result_label, result_score    
    
    def __get_label_and_score_with_max_score(self, data):
        # 使用 max 函數找到 score 最高的字典
        max_score_dict = max(data, key=lambda x: x['score'])

        # 獲取對應的 label 和 score
        label_with_max_score = max_score_dict['label']
        score_with_max_score = max_score_dict['score']

        return label_with_max_score, score_with_max_score  

    def __is_need_to_connect_mqtt(self, mqtt_host):
        if mqtt_host and mqtt_host.strip():
            return True
        return False      
    
    def __get_mqtt_client(self, mqtt_host, mqtt_topic):
        if mqtt_host and not mqtt_host.strip():
            raise AppError(message="mqtt topic is empty.")
        
        mqtt_client = mqtt.Client()
        try:
            mqtt_client.username_pw_set("admin", "admin")
            mqtt_client.connect(mqtt_host, 1883)
        except:
            print("Error connecting to MQTT broker.")
            raise AppError(message="Error connecting to MQTT broker.")
        
        return mqtt_client
    
    def __put_thread_info(self, input: 'InferenceService.ClassifyStreamingInputDto'):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Remove the last 3 characters
        info = {
            "id": self.pipeline_sequential_id,
            "state": "RUNNING",
            "avg_fps": 0,
            "start_time": timestamp,    
            "source_uri": input.uri,
            "destination_mqtt_host": input.mqtt_host,
            "destination_mqtt_topic": input.mqtt_topic,
            "device_name": input.device_name,
            "message": ""
        }
        self.thread_info[self.pipeline_sequential_id] = info    

    def __set_thread_info_message(self, pipeline_id, message):
        self.thread_info[pipeline_id]['state'] = "ERROR"
        self.thread_info[pipeline_id]['message'] = message    

    class ClassifyStreamingInputDto(BaseModel):
        uri: str = Field(..., description="The uri is required.")
        device_name: str
        mqtt_host: str
        mqtt_topic: str

    class GetPipelinesOutputDto(BaseModel):
        id: int
        state: str
        avg_fps: float
        start_time: str
        source_uri: str
        destination_mqtt_host: str
        destination_mqtt_topic: str
        device_name: str
        message: str
