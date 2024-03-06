from pydantic import BaseModel


class Rectangle(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    text: str
    id: int