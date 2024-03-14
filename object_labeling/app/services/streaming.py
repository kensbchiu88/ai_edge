
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.db.repositories.streaming import StreamingRepository


class StreamingService:
    def __init__(self, session):
        self.streaming_repository = StreamingRepository(session)

    def get_streaming(self) -> List['StreamingService.Streaming']:
        streaming_list = self.streaming_repository.get_streaming()

        streaming_dto_list = []
        for streaming_schema in streaming_list:
            streaming_dto = StreamingService.StreamingDto(id=streaming_schema.id, uri=streaming_schema.uri, device_name=streaming_schema.device_name, create_time=streaming_schema.create_time)
            streaming_dto_list.append(streaming_dto)

        return streaming_dto_list
    
    def get_streaming_by_uri(self, uri) -> Optional['StreamingService.Streaming']:
        streaming_schema = self.streaming_repository.get_streaming_by_uri(uri)
        if(streaming_schema):
            return StreamingService.StreamingDto(id=streaming_schema.id, uri=streaming_schema.uri, device_name=streaming_schema.device_name, create_time=streaming_schema.create_time)
    
    def get_id_by_uri(self, uri) -> Optional[int]:
        streaming = self.streaming_repository.get_streaming_by_uri(uri)
        if(streaming):
            return streaming.id
        return None
    
    class StreamingDto(BaseModel):
        id: int
        uri: str
        device_name: str
        create_time: datetime