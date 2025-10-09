from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.workout import get_workout_summary, get_workouts
from app.schemas.workout import (
    ActiveEnergyValue,
    DateRange,
    DistanceValue,
    HumidityValue,
    IntensityValue,
    TemperatureValue,
    WorkoutListResponse,
    WorkoutMeta,
    WorkoutQueryParams,
    WorkoutResponse,
    WorkoutSummary,
)

router = APIRouter()


@router.get("/workouts", response_model=WorkoutListResponse)
async def get_workouts_endpoint(
    start_date: Optional[str] = Query(
        None, description="ISO 8601 format (e.g., '2023-12-01T00:00:00Z')"
    ),
    end_date: Optional[str] = Query(
        None, description="ISO 8601 format (e.g., '2023-12-31T23:59:59Z')"
    ),
    workout_type: Optional[str] = Query(
        None, description="e.g., 'Outdoor Walk', 'Indoor Walk'"
    ),
    location: Optional[str] = Query(None, description="Indoor or Outdoor"),
    min_duration: Optional[int] = Query(None, description="in seconds"),
    max_duration: Optional[int] = Query(None, description="in seconds"),
    min_distance: Optional[float] = Query(None, description="in km"),
    max_distance: Optional[float] = Query(None, description="in km"),
    sort_by: str = Query("date", description="Sort field"),
    sort_order: str = Query("desc", description="Sort order"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    db: Session = Depends(get_db),
):
    """Get workouts with filtering, sorting, and pagination."""

    # Create query parameters object
    query_params = WorkoutQueryParams(
        start_date=start_date,
        end_date=end_date,
        workout_type=workout_type,
        location=location,
        min_duration=min_duration,
        max_duration=max_duration,
        min_distance=min_distance,
        max_distance=max_distance,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )

    # Get workouts from database
    workouts, total_count = get_workouts(db, query_params)

    # Convert workouts to response format
    workout_responses = []
    for workout in workouts:
        # Get summary data
        summary_data = get_workout_summary(db, workout.id)

        # Build response object
        workout_response = WorkoutResponse(
            id=workout.id,
            name=workout.name or "Unknown Workout",
            location=workout.location or "Outdoor",
            start=workout.start.isoformat(),
            end=workout.end.isoformat(),
            duration=int(workout.duration or 0),
            distance=DistanceValue(
                value=float(workout.distance_qty or 0),
                unit=workout.distance_units or "km",
            ),
            active_energy_burned=ActiveEnergyValue(
                value=float(workout.active_energy_burned_qty or 0),
                unit=workout.active_energy_burned_units or "kJ",
            ),
            intensity=IntensityValue(
                value=float(workout.intensity_qty or 0),
                unit=workout.intensity_units or "kcal/hr·kg",
            ),
            temperature=(
                TemperatureValue(
                    value=float(workout.temperature_qty or 0),
                    unit=workout.temperature_units or "degC",
                )
                if workout.temperature_qty
                else None
            ),
            humidity=(
                HumidityValue(
                    value=float(workout.humidity_qty or 0),
                    unit=workout.humidity_units or "%",
                )
                if workout.humidity_qty
                else None
            ),
            source="Apple Health",  # Default source
            summary=WorkoutSummary(**summary_data),
        )
        workout_responses.append(workout_response)

    # Calculate date range
    date_range = DateRange(
        start=start_date or "1900-01-01T00:00:00Z",
        end=end_date or datetime.now().isoformat() + "Z",
        duration_days=0,  # This would need to be calculated based on actual date range
    )

    # Build metadata
    meta = WorkoutMeta(
        requested_at=datetime.now().isoformat() + "Z",
        filters={
            "start_date": start_date,
            "end_date": end_date,
            "workout_type": workout_type,
            "location": location,
            "min_duration": min_duration,
            "max_duration": max_duration,
            "min_distance": min_distance,
            "max_distance": max_distance,
        },
        result_count=total_count,
        date_range=date_range,
    )

    return WorkoutListResponse(
        data=workout_responses,
        meta=meta,
    )
