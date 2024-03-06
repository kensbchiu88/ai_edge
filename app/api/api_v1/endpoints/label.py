from typing import List
from fastapi import APIRouter
from app.api.api_v1.models.save_label_request import SaveLabelRequest
from app.api.api_v1.models.streaming_response import StreamingResponse
from app.api.dependencies.database import SessionDep

#from app.api.api_v1.models.Rectangle import Rectangle
from app.services.label import LabelService
from app.api.api_v1.models.labels import Labels
from app.services.streaming import StreamingService

router = APIRouter()

@router.get("/streaming_data", response_model=List[StreamingResponse])
async def get_streaming_data(session: SessionDep):
    streaming_service = StreamingService(session)
    streaming_dto_list = streaming_service.get_streaming()

    response = []
    for dto in streaming_dto_list:  
        response.append(dto.model_dump())

    return response

@router.post("/labels/")
async def save_labels(session: SessionDep, request: List[SaveLabelRequest]):
    label_dto_list = []
    for label_request in request:
        print(label_request)
        label_dto = LabelService.LabelInsertDto(**label_request.model_dump())
        label_dto_list.append(label_dto)

    label_service = LabelService(session)
    label_service.insert_labels(label_dto_list)

@router.get("/labels", response_model= Labels)
async def get_rectangle(session: SessionDep):
    label_service = LabelService(session)
    labels = label_service.get_labels(1)
    print()
    
    #return {"equipment_no": labels.equipment_no}
    return labels

@router.get("/test1")
async def test():
    return {"message": "Hello World"}
