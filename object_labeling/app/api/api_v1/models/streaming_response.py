
from datetime import datetime
from pydantic import BaseModel


class StreamingResponse(BaseModel):
    id: int
    uri: str
    device_name: str
    create_time: datetime