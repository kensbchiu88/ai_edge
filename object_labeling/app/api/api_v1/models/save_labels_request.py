
from pydantic import BaseModel


class SaveLabelsRequest(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    equipment_no: str
    streaming_data_id: int
    type: str