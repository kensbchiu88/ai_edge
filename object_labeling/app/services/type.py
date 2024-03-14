
from datetime import datetime
from typing import List
from pydantic import BaseModel
from app.db.repositories.type import TypeRepository


class TypeService:
    def __init__(self, session):
        self.type_repository = TypeRepository(session)

    def get_types(self) -> List['TypeService.TypeDto']:
        type_list = self.type_repository.get_types()

        type_dto_list = []
        for type_schema in type_list:
            type_dto = TypeService.TypeDto(key=type_schema.key, text=type_schema.text, create_time=type_schema.create_time)
            type_dto_list.append(type_dto)

        return type_dto_list
    
    class TypeDto(BaseModel):
        key: str
        text: str
        create_time: datetime