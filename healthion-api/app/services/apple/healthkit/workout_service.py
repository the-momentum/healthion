from logging import Logger, getLogger
from uuid import UUID

from app.database import DbSession
from app.models import Workout
from app.repositories import HKWorkoutRepository
from app.schemas import (
    HKWorkoutCreate,
    HKWorkoutUpdate,

)
from app.services import AppService
from app.utils.exceptions import handle_exceptions


class WorkoutService(AppService[HKWorkoutRepository, Workout, HKWorkoutCreate, HKWorkoutUpdate]):
    """Service for workout-related business logic."""

    def __init__(self, log: Logger, **kwargs):
        super().__init__(
            crud_model=HKWorkoutRepository,
            model=Workout,
            log=log,
            **kwargs
        )

    @handle_exceptions
    async def _get_workouts_with_filters(
            self,
            db_session: DbSession,
            query_params,
            user_id: str
    ) -> tuple[list[Workout], int]:
        """
        Get workouts with filtering, sorting, and pagination.
        Includes business logic and logging.
        """
        pass

    @handle_exceptions
    async def _get_workout_with_summary(
            self,
            db_session: DbSession,
            workout_id: UUID
    ) -> tuple[Workout | None, dict]:
        """
        Get a single workout with its summary statistics.
        """
        pass

    @handle_exceptions
    async def get_workouts_response(
            self,
            db_session: DbSession,
            query_params,
            user_id: str
    ):
        """
        Get workouts formatted as API response.

        Returns:
            WorkoutListResponse ready for API
        """
        pass


workout_service = WorkoutService(log=getLogger(__name__))
