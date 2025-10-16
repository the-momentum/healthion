from typing import Annotated

from fastapi import APIRouter, Depends

from app.utils.auth_dependencies import get_current_user_id
from app.database import DbSession
from app.schemas import WorkoutListResponse, WorkoutQueryParams
from app.services import workout_service

router = APIRouter()


@router.get("/workouts", response_model=WorkoutListResponse)
async def get_workouts_endpoint(
    db: DbSession,
    user_id: Annotated[str, Depends(get_current_user_id)],
    query_params: WorkoutQueryParams = Depends(),
):
    """Get workouts with filtering, sorting, and pagination."""
    return await workout_service.get_workouts_response(db, query_params, user_id)
