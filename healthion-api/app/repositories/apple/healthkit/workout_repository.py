from uuid import UUID

from app.database import DbSession
from app.models import Workout
from app.repositories import CrudRepository
from app.schemas import AEWorkoutQueryParams, HKWorkoutCreate, HKWorkoutUpdate


class WorkoutRepository(CrudRepository[Workout, HKWorkoutCreate, HKWorkoutUpdate]):
    def __init__(self, model: type[Workout]):
        super().__init__(model)

    def get_workouts_with_filters(
        self,
        db_session: DbSession,
        query_params: AEWorkoutQueryParams,
        user_id: str
    ) -> tuple[list[Workout], int]:
        pass

    def get_workout_summary(self, db_session: DbSession, workout_id: UUID) -> dict:
        pass
