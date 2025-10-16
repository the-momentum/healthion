from uuid import UUID

from app.database import DbSession
from app.models.active_energy import ActiveEnergy
from app.repositories.repositories import CrudRepository
from app.schemas.active_energy import ActiveEnergyCreate, ActiveEnergyUpdate


class ActiveEnergyRepository(CrudRepository[ActiveEnergy, ActiveEnergyCreate, ActiveEnergyUpdate]):
    def __init__(self, model: type[ActiveEnergy]):
        super().__init__(model)

    def get_active_energy_by_workout_id(self, db_session: DbSession, workout_id: UUID) -> list[ActiveEnergy]:
        return db_session.query(self.model).filter(self.model.workout_id == workout_id).all()

    def get_active_energy_by_user_id(self, db_session: DbSession, user_id: str) -> list[ActiveEnergy]:
        return db_session.query(self.model).filter(self.model.user_id == user_id).all()
