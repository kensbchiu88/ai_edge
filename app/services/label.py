
from typing import List
from pydantic import BaseModel
from app.db.repositories.label import LabelRepository
from app.db.schemas.label import Label as LabelsSchema


class LabelService:
    def __init__(self, session):
        self.label_repository = LabelRepository(session)
        
    def get_labels(self, streaming_id):
        label_schema_list = self.label_repository.get_labels_by_streaming_id(streaming_id)
        label_dto_list = []
        for label_schema in label_schema_list:
            label_dto = LabelService.LabelDto(id=label_schema.id, streaming_data_id=label_schema.streaming_data_id, equipment_no=label_schema.equipment_no, x1=label_schema.x1, y1=label_schema.y1, x2=label_schema.x2, y2=label_schema.y2)
            label_dto_list.append(label_dto)
        
        return label_dto_list

    def get_labels_by_uri(self, uri):
        label_schema_list = self.label_repository.get_labels_by_uri(uri)
        label_dto_list = []
        for label_schema in label_schema_list:
            label_dto = LabelService.LabelDto(id=label_schema.id, streaming_data_id=label_schema.streaming_data_id, equipment_no=label_schema.equipment_no, x1=label_schema.x1, y1=label_schema.y1, x2=label_schema.x2, y2=label_schema.y2)
            label_dto_list.append(label_dto)
        
        return label_dto_list

    
    def delete_labels(self, streaming_id):
        self.label_repository.delete_labels_by_streaming_id(streaming_id)

    def insert_labels(self, label_dto_list: List['LabelService.LabelInsertDto']):
        if(len(label_dto_list) > 0):
            streaming_data_id = label_dto_list[0].streaming_data_id
            self.label_repository.delete_labels_by_streaming_id(streaming_data_id)
            label_schema_list = list()
            for label_dto in label_dto_list:
                label_schema_list.append(LabelsSchema(**label_dto.dict()))

            self.label_repository.save(label_schema_list)

    class LabelDto(BaseModel):
        id: int
        streaming_data_id: int
        equipment_no: str
        x1: int
        y1: int
        x2: int
        y2: int

    class LabelInsertDto(BaseModel):
        streaming_data_id: int
        equipment_no: str
        x1: int
        y1: int
        x2: int
        y2: int        
