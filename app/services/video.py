import os
import cv2
import uuid

from app.core.error import AppError
class VideoService:

    def save_frame_as_image(self, uri):
        cap = cv2.VideoCapture(uri)
        success, frame = cap.read()
        cap.release()

        if not success:
            raise AppError("Unable to read video file")
        
        # 将视频的第一帧保存为临时图像文件
        temp_img_path = os.path.join("temp/", str(uuid.uuid4()) + ".jpg")
        cv2.imwrite(temp_img_path, frame)
        print(temp_img_path)
        return temp_img_path