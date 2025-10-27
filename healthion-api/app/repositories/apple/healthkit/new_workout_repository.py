from uuid import UUID

from app.database import DbSession
from app.models import NewWorkout
from app.repositories import CrudRepository
from app.schemas import WorkoutQueryParams, HKWorkoutCreate, HKWorkoutUpdate


class WorkoutRepository(CrudRepository[NewWorkout, HKWorkoutCreate, HKWorkoutUpdate]):
    def __init__(self, model: type[NewWorkout]):
        super().__init__(model)

    def get_workouts_with_filters(
        self,
        db_session: DbSession,
        query_params: WorkoutQueryParams,
        user_id: str
    ) -> tuple[list[NewWorkout], int]:
        pass

    def get_workout_summary(self, db_session: DbSession, workout_id: UUID) -> dict:
        pass
