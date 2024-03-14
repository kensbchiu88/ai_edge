from fastapi import APIRouter
from app.api.api_v1.endpoints.label import router as label_router


router = APIRouter()

router.include_router(label_router, tags=["label"])


