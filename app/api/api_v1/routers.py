from fastapi import APIRouter
from app.api.api_v1.endpoints.label import router as label_router
from app.api.api_v1.endpoints.inference import router as inference_router


router = APIRouter()

router.include_router(label_router, tags=["label"])
router.include_router(inference_router, tags=["inference"])


