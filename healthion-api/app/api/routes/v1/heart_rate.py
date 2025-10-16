from typing import Annotated

from fastapi import APIRouter, Depends

from app.utils.auth_dependencies import get_current_user_id
from app.database import DbSession
from app.schemas import HeartRateListResponse, HeartRateQueryParams
from app.services import heart_rate_service

router = APIRouter()


@router.get("/heart-rate", response_model=HeartRateListResponse)
async def get_heart_rate_endpoint(
    db: DbSession,
    user_id: Annotated[str, Depends(get_current_user_id)],
    query_params: HeartRateQueryParams = Depends(),
):
    """Get heart rate data with filtering, sorting, and pagination."""
    return await heart_rate_service.buil_heart_rate_full_data_response(db, query_params, user_id)
