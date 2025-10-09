from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.heart_rate import (
    get_heart_rate_data,
    get_heart_rate_recovery_data,
    get_heart_rate_summary,
)
from app.schemas.heart_rate import (
    HeartRateDataResponse,
    HeartRateListResponse,
    HeartRateMeta,
    HeartRateQueryParams,
    HeartRateRecoveryResponse,
    HeartRateSummary,
    HeartRateValue,
)

router = APIRouter()


@router.get("/heart-rate", response_model=HeartRateListResponse)
async def get_heart_rate_endpoint(
    start_date: Optional[str] = Query(
        None, description="ISO 8601 format (e.g., '2023-12-01T00:00:00Z')"
    ),
    end_date: Optional[str] = Query(
        None, description="ISO 8601 format (e.g., '2023-12-31T23:59:59Z')"
    ),
    workout_id: Optional[UUID] = Query(
        None, description="Filter by specific workout ID"
    ),
    source: Optional[str] = Query(
        None, description="Filter by data source (e.g., 'Apple Health')"
    ),
    min_avg: Optional[float] = Query(None, description="Minimum average heart rate"),
    max_avg: Optional[float] = Query(None, description="Maximum average heart rate"),
    min_max: Optional[float] = Query(None, description="Minimum maximum heart rate"),
    max_max: Optional[float] = Query(None, description="Maximum maximum heart rate"),
    min_min: Optional[float] = Query(None, description="Minimum minimum heart rate"),
    max_min: Optional[float] = Query(None, description="Maximum minimum heart rate"),
    sort_by: str = Query("date", description="Sort field"),
    sort_order: str = Query("desc", description="Sort order"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
):
    """Get heart rate data with filtering, sorting, and pagination."""

    # Create query parameters object
    query_params = HeartRateQueryParams(
        start_date=start_date,
        end_date=end_date,
        workout_id=workout_id,
        source=source,
        min_avg=min_avg,
        max_avg=max_avg,
        min_max=min_max,
        max_max=max_max,
        min_min=min_min,
        max_min=max_min,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )

    # Get heart rate data from database
    heart_rate_data, hr_total_count = get_heart_rate_data(db, query_params)
    heart_rate_recovery_data, hr_recovery_total_count = get_heart_rate_recovery_data(
        db, query_params
    )

    # Get summary statistics
    summary_data = get_heart_rate_summary(db, query_params)

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
        filters={
            "start_date": start_date,
            "end_date": end_date,
            "workout_id": str(workout_id) if workout_id else None,
            "source": source,
            "min_avg": min_avg,
            "max_avg": max_avg,
            "min_max": min_max,
            "max_max": max_max,
            "min_min": min_min,
            "max_min": max_min,
        },
        result_count=hr_total_count + hr_recovery_total_count,
        date_range={
            "start": start_date or "1900-01-01T00:00:00Z",
            "end": end_date or datetime.now().isoformat() + "Z",
        },
    )

    return HeartRateListResponse(
        data=heart_rate_responses,
        recovery_data=heart_rate_recovery_responses,
        summary=summary,
        meta=meta,
    )
