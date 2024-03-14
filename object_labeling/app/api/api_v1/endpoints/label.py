from typing import List, Optional
from fastapi import APIRouter, Query
from app.api.api_v1.models.get_types_response import GetTypesResponse
from app.api.api_v1.models.save_labels_request import SaveLabelsRequest
from app.api.api_v1.models.streaming_response import StreamingResponse
from app.api.dependencies.database import SessionDep

#from app.api.api_v1.models.Rectangle import Rectangle
from app.services.label import LabelService
from app.api.api_v1.models.get_label_response import GetLabelResponse
from app.services.streaming import StreamingService
from app.services.type import TypeService

router = APIRouter()

@router.get("/streaming", response_model=List[StreamingResponse])
async def get_streaming_data_by_uri(session: SessionDep, uri: Optional[str] = None):
    streaming_service = StreamingService(session)
    response = []
    if uri:
        streaming_dto = streaming_service.get_streaming_by_uri(uri)
        response.append(streaming_dto.model_dump())
    else:
        streaming_dto_list = streaming_service.get_streaming()
        for dto in streaming_dto_list:
            response.append(dto.model_dump())

    return response

@router.post("/labels/")
async def save_labels(session: SessionDep, request: List[SaveLabelsRequest]):
    label_dto_list = []
    for label_request in request:
        label_dto = LabelService.LabelInsertDto(**label_request.model_dump())
        label_dto_list.append(label_dto)

    label_service = LabelService(session)
    label_service.insert_labels(label_dto_list)

@router.get("/streaming/{id}/labels", response_model= List[GetLabelResponse])
async def get_rectangle(session: SessionDep, id: int):
    label_service = LabelService(session)
    labels = label_service.get_labels(id)

    return labels

@router.get("/types", response_model=List[GetTypesResponse])
async def get_type_data(session: SessionDep):
    type_service = TypeService(session)
    type_dto_list = type_service.get_types()

    response = []
    for dto in type_dto_list:  
        response.append(dto.model_dump())

    return response
