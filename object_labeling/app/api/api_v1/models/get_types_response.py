from pydantic import BaseModel

class GetTypesResponse(BaseModel):
    key: str
    text: str