from fastapi import APIRouter

from .auth import router as auth_router
from .heart_rate import router as heart_rate_router
from .workouts import router as workouts_router
from .import_data import router as import_data_router
from .fake_import import router as fake_import_router

v1_router = APIRouter()
v1_router.include_router(auth_router, tags=["auth"])
v1_router.include_router(heart_rate_router, tags=["heart-rate"])
v1_router.include_router(workouts_router, tags=["workout"])
v1_router.include_router(import_data_router, tags=["import-data"])
v1_router.include_router(fake_import_router, tags=["fake-import"])

__all__ = ["v1_router"]
