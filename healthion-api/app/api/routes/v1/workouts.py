from datetime import datetime
from logging import getLogger

from fastapi import APIRouter, Depends

from app.database import DbSession
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
from app.services.workout_service import WorkoutService

router = APIRouter()


@router.get("/workouts", response_model=WorkoutListResponse)
async def get_workouts_endpoint(
    db: DbSession,
    query_params: WorkoutQueryParams = Depends(),
    workout_service: WorkoutService = Depends(lambda: WorkoutService(log=getLogger(__name__))),
):
    """Get workouts with filtering, sorting, and pagination."""

    # Get workouts from service
    workouts, total_count = workout_service.get_workouts_with_filters(db, query_params)

    # Convert workouts to response format
    workout_responses = []
    for workout in workouts:
        # Get summary data
        _, summary_data = workout_service.get_workout_with_summary(db, workout.id)

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
        start=query_params.start_date or "1900-01-01T00:00:00Z",
        end=query_params.end_date or datetime.now().isoformat() + "Z",
        duration_days=0,  # This would need to be calculated based on actual date range
    )

    # Build metadata
    meta = WorkoutMeta(
        requested_at=datetime.now().isoformat() + "Z",
        filters=query_params.model_dump(exclude_none=True),
        result_count=total_count,
        date_range=date_range,
    )

    return WorkoutListResponse(
        data=workout_responses,
        meta=meta,
    )
