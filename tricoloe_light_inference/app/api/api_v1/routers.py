from fastapi import APIRouter
from app.api.api_v1.endpoints.inference import router as inference_router


router = APIRouter()

router.include_router(inference_router, tags=["inference"])


