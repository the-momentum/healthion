from datetime import datetime
from logging import getLogger

from fastapi import APIRouter, Depends

from app.database import DbSession
from app.schemas.heart_rate import (
    HeartRateDataResponse,
    HeartRateListResponse,
    HeartRateMeta,
    HeartRateQueryParams,
    HeartRateRecoveryResponse,
    HeartRateSummary,
    HeartRateValue,
)
from app.services.heart_rate_service import HeartRateService

router = APIRouter()


@router.get("/heart-rate", response_model=HeartRateListResponse)
async def get_heart_rate_endpoint(
    db: DbSession,
    query_params: HeartRateQueryParams = Depends(),
    heart_rate_service: HeartRateService = Depends(lambda: HeartRateService(log=getLogger(__name__))),
):
    """Get heart rate data with filtering, sorting, and pagination."""

    # Get complete heart rate data from service
    heart_rate_data, heart_rate_recovery_data, summary_data, hr_total_count, hr_recovery_total_count = heart_rate_service.get_complete_heart_rate_data(db, query_params)

    # Convert heart rate data to response format
    heart_rate_responses = []
    for hr_data in heart_rate_data:
        heart_rate_response = HeartRateDataResponse(
            id=hr_data.id,
            workout_id=hr_data.workout_id,
            date=hr_data.date.isoformat(),
            source=hr_data.source,
            units=hr_data.units,
            avg=(
                HeartRateValue(
                    value=float(hr_data.avg or 0),
                    unit=hr_data.units or "bpm",
                )
                if hr_data.avg
                else None
            ),
            min=(
                HeartRateValue(
                    value=float(hr_data.min or 0),
                    unit=hr_data.units or "bpm",
                )
                if hr_data.min
                else None
            ),
            max=(
                HeartRateValue(
                    value=float(hr_data.max or 0),
                    unit=hr_data.units or "bpm",
                )
                if hr_data.max
                else None
            ),
        )
        heart_rate_responses.append(heart_rate_response)

    # Convert heart rate recovery data to response format
    heart_rate_recovery_responses = []
    for hr_recovery_data in heart_rate_recovery_data:
        heart_rate_recovery_response = HeartRateRecoveryResponse(
            id=hr_recovery_data.id,
            workout_id=hr_recovery_data.workout_id,
            date=hr_recovery_data.date.isoformat(),
            source=hr_recovery_data.source,
            units=hr_recovery_data.units,
            avg=(
                HeartRateValue(
                    value=float(hr_recovery_data.avg or 0),
                    unit=hr_recovery_data.units or "bpm",
                )
                if hr_recovery_data.avg
                else None
            ),
            min=(
                HeartRateValue(
                    value=float(hr_recovery_data.min or 0),
                    unit=hr_recovery_data.units or "bpm",
                )
                if hr_recovery_data.min
                else None
            ),
            max=(
                HeartRateValue(
                    value=float(hr_recovery_data.max or 0),
                    unit=hr_recovery_data.units or "bpm",
                )
                if hr_recovery_data.max
                else None
            ),
        )
        heart_rate_recovery_responses.append(heart_rate_recovery_response)

    # Build summary
    summary = HeartRateSummary(**summary_data)

    # Build metadata
    meta = HeartRateMeta(
        requested_at=datetime.now().isoformat() + "Z",
        filters=query_params.model_dump(exclude_none=True),
        result_count=hr_total_count + hr_recovery_total_count,
        date_range={
            "start": query_params.start_date or "1900-01-01T00:00:00Z",
            "end": query_params.end_date or datetime.now().isoformat() + "Z",
        },
    )

    return HeartRateListResponse(
        data=heart_rate_responses,
        recovery_data=heart_rate_recovery_responses,
        summary=summary,
        meta=meta,
    )
