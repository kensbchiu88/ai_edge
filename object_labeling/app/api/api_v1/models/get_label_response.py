from pydantic import BaseModel

class GetLabelResponse(BaseModel):
    id: int
    streaming_data_id: int
    equipment_no: str
    x1: int
    y1: int
    x2: int
    y2: int
    type: str

    class Config:
        from_attributes = True

