from fastapi import APIRouter

from app.api.routes.v1.heart_rate import router as heart_rate_router_v1
from app.api.routes.v1.workouts import router as workouts_router_v1
from app.api.routes.v1.import_data import router as import_data_router_v1


head_router = APIRouter()
head_router.include_router(heart_rate_router_v1, prefix="", tags=["heart_rate"])
head_router.include_router(workouts_router_v1, prefix="", tags=["workouts"])
head_router.include_router(import_data_router_v1, prefix="/import_data", tags=["import_data"])

__all__ = [
    "head_router",
]