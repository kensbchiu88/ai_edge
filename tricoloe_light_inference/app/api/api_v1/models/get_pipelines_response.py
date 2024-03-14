from pydantic import BaseModel


class GetPipelinesResponseModel(BaseModel):
    id: int
    state: str
    avg_fps: float
    start_time: str
    source_uri: str
    destination_mqtt_host: str
    destination_mqtt_topic: str
    device_name: str
    message: str