from datetime import datetime
from fastapi import APIRouter
from app.api.api_v1.models.get_pipelines_response import GetPipelinesResponseModel

from app.api.dependencies.database import SessionDep
from app.services.inference import InferenceService

router = APIRouter()

# singleton object
inference_service = InferenceService()

@router.post("/pipeline")
async def start_pipeline(session: SessionDep, data: dict):
    classify_streaming_input_dto = InferenceService.ClassifyStreamingInputDto(**data)
    try:
        inference_service.start_pipeline(session, classify_streaming_input_dto)
        return {"message": f"Processing URI: {classify_streaming_input_dto.uri}"}
    except Exception as e:  
        return {"message": str(e)}
    
@router.delete("/pipeline/{pipeline_id}")
async def stop_pipeline(pipeline_id: int):
    try:
        inference_service.stop_pipeline(pipeline_id)
        return {"message": f"Stop Processing URI: {inference_service.get_uri_by_pipeline_id(pipeline_id)}"}
    except Exception as e:
        return {"message": str(e)} 
    
@router.get("/pipelines/", response_model=list[GetPipelinesResponseModel])    
async def show_pipelines():
    return inference_service.get_pipelines()