from pydantic import BaseModel

class Labels(BaseModel):
    id: int
    streaming_data_id: int
    equipment_no: str
    x1: int
    y1: int
    x2: int
    y2: int

    class Config:
        orm_mode = True

