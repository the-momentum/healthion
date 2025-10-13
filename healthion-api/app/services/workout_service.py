from logging import Logger
from uuid import UUID

from app.database import DbSession
from app.models.workout import Workout
from app.repositories.workout_repository import WorkoutRepository
from app.schemas.workout import WorkoutQueryParams
from app.schemas.workout import WorkoutCreate, WorkoutUpdate
from app.services.services import AppService


class WorkoutService(AppService[WorkoutRepository, Workout, WorkoutCreate, WorkoutUpdate]):
    """Service for workout-related business logic."""

    def __init__(self, log: Logger, **kwargs):
        super().__init__(
            crud_model=WorkoutRepository,
            model=Workout,
            log=log,
            **kwargs
        )

    def get_workouts_with_filters(
        self, 
        db_session: DbSession, 
        query_params: WorkoutQueryParams,
        user_id: UUID | None = None
    ) -> tuple[list[Workout], int]:
        """
        Get workouts with filtering, sorting, and pagination.
        Includes business logic and logging.
        """
        self.logger.info(f"Fetching workouts with filters: {query_params.model_dump()}")
        
        workouts, total_count = self.crud.get_workouts_with_filters(
            db_session, query_params, user_id
        )
        
        self.logger.info(f"Retrieved {len(workouts)} workouts out of {total_count} total")
        
        return workouts, total_count

    def get_workout_with_summary(
        self, 
        db_session: DbSession, 
        workout_id: UUID
    ) -> tuple[Workout | None, dict]:
        """
        Get a single workout with its summary statistics.
        """
        self.logger.info(f"Fetching workout {workout_id} with summary")
        
        workout = self.get(db_session, workout_id, raise_404=True)
        summary = self.crud.get_workout_summary(db_session, workout_id)
        
        self.logger.info(f"Retrieved workout {workout_id} with summary data")
        
        return workout, summary
