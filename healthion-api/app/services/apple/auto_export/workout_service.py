from datetime import datetime
from logging import Logger, getLogger
from uuid import UUID

from app.database import DbSession
from app.models import Workout
from app.repositories import WorkoutRepository
from app.schemas import (
    WorkoutQueryParams, 
    AEWorkoutCreate, 
    AEWorkoutUpdate,
    WorkoutListResponse,
    AEWorkoutResponse,
    AESummary,
    AEMeta,
    DistanceValue,
    AEActiveEnergyValue,
    AEIntensityValue,
    AETemperatureValue,
    AEHumidityValue,
    DateRange,
)
from app.services import AppService
from app.utils.exceptions import handle_exceptions


class WorkoutService(AppService[WorkoutRepository, Workout, AEWorkoutCreate, AEWorkoutUpdate]):
    """Service for workout-related business logic."""

    def __init__(self, log: Logger, **kwargs):
        super().__init__(
            crud_model=WorkoutRepository,
            model=Workout,
            log=log,
            **kwargs
        )

    @handle_exceptions
    async def _get_workouts_with_filters(
        self, 
        db_session: DbSession, 
        query_params: WorkoutQueryParams,
        user_id: str
    ) -> tuple[list[Workout], int]:
        """
        Get workouts with filtering, sorting, and pagination.
        Includes business logic and logging.
        """
        self.logger.debug(f"Fetching workouts with filters: {query_params.model_dump()}")
        
        workouts, total_count = self.crud.get_workouts_with_filters(
            db_session, query_params, user_id
        )
        
        self.logger.debug(f"Retrieved {len(workouts)} workouts out of {total_count} total")
        
        return workouts, total_count

    @handle_exceptions
    async def _get_workout_with_summary(
        self, 
        db_session: DbSession, 
        workout_id: UUID
    ) -> tuple[Workout | None, dict]:
        """
        Get a single workout with its summary statistics.
        """
        self.logger.debug(f"Fetching workout {workout_id} with summary")
        
        workout = self.get(db_session, workout_id, raise_404=True)
        summary = self.crud.get_workout_summary(db_session, workout_id)
        
        self.logger.debug(f"Retrieved workout {workout_id} with summary data")
        
        return workout, summary

    @handle_exceptions
    async def get_workouts_response(
        self, 
        db_session: DbSession, 
        query_params: WorkoutQueryParams,
        user_id: str
    ) -> WorkoutListResponse:
        """
        Get workouts formatted as API response.
        
        Returns:
            WorkoutListResponse ready for API
        """
        # Get raw data
        workouts, total_count = await self._get_workouts_with_filters(db_session, query_params, user_id)
        
        # Convert workouts to response format
        workout_responses = []
        for workout in workouts:
            # Get summary data
            _, summary_data = await self._get_workout_with_summary(db_session, workout.id)
            
            # Build response object
            workout_response = AEWorkoutResponse(
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
                active_energy_burned=AEActiveEnergyValue(
                    value=float(workout.active_energy_burned_qty or 0),
                    unit=workout.active_energy_burned_units or "kJ",
                ),
                intensity=AEIntensityValue(
                    value=float(workout.intensity_qty or 0),
                    unit=workout.intensity_units or "kcal/hr·kg",
                ),
                temperature=(
                    AETemperatureValue(
                        value=float(workout.temperature_qty or 0),
                        unit=workout.temperature_units or "°C",
                    )
                    if workout.temperature_qty
                    else None
                ),
                humidity=(
                    AEHumidityValue(
                        value=float(workout.humidity_qty or 0),
                        unit=workout.humidity_units or "%",
                    )
                    if workout.humidity_qty
                    else None
                ),
                summary=AESummary(**summary_data),
            )
            workout_responses.append(workout_response)

        # Calculate date range and duration
        start_date_str = query_params.start_date or "1900-01-01T00:00:00Z"
        end_date_str = query_params.end_date or datetime.now().isoformat() + "Z"
        
        # Parse dates to calculate duration
        start_date = datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))
        end_date = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
        duration_days = (end_date - start_date).days
        
        # Build metadata
        meta = AEMeta(
            requested_at=datetime.now().isoformat() + "Z",
            filters=query_params.model_dump(exclude_none=True),
            result_count=total_count,
            date_range=DateRange(
                start=start_date_str,
                end=end_date_str,
                duration_days=duration_days,
            ),
        )

        return WorkoutListResponse(
            data=workout_responses,
            meta=meta,
        )


workout_service = WorkoutService(log=getLogger(__name__))
