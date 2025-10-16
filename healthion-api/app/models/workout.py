from uuid import UUID

from sqlalchemy.orm import Mapped

from app.database import BaseDbModel
from app.mappings import (
    FKUser,
    ManyToOne,
    OneToMany,
    PrimaryKey,
    datetime_tz,
    numeric_10_2,
    numeric_15_5,
    str_10,
    str_100,
    str_255,
    str_50,
)


class Workout(BaseDbModel):
    id: Mapped[PrimaryKey[UUID]]
    user_id: Mapped[FKUser]
    name: Mapped[str_255 | None]
    location: Mapped[str_100 | None]
    start: Mapped[datetime_tz]
    end: Mapped[datetime_tz]
    duration: Mapped[numeric_15_5 | None]

    active_energy_burned_qty: Mapped[numeric_15_5 | None]
    active_energy_burned_units: Mapped[str_50 | None]
    distance_qty: Mapped[numeric_15_5 | None]
    distance_units: Mapped[str_50 | None]
    intensity_qty: Mapped[numeric_15_5 | None]
    intensity_units: Mapped[str_50 | None]
    humidity_qty: Mapped[numeric_10_2 | None]
    humidity_units: Mapped[str_10 | None]
    temperature_qty: Mapped[numeric_10_2 | None]
    temperature_units: Mapped[str_10 | None]

    user: Mapped[ManyToOne["User"]]
    heart_rate_data: Mapped[OneToMany["HeartRateData"]]
    heart_rate_recovery: Mapped[OneToMany["HeartRateRecovery"]]
    active_energy: Mapped[OneToMany["ActiveEnergy"]]
