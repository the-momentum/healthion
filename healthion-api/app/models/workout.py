from uuid import UUID

from sqlalchemy.orm import Mapped

from app.database import BaseDbModel
from app.mappings import (
    OneToMany,
    PrimaryKey,
    datetime_tz,
    numeric_10_2,
    numeric_15_5,
    rel_attr_cascade,
    str_10,
    str_100,
    str_255,
    str_50,
)


class Workout(BaseDbModel):
    id: Mapped[PrimaryKey[UUID]]
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

    heart_rate_data: Mapped[OneToMany["HeartRateData"]] = rel_attr_cascade("workout")
    heart_rate_recovery: Mapped[OneToMany["HeartRateRecovery"]] = rel_attr_cascade("workout")
    active_energy: Mapped[OneToMany["ActiveEnergy"]] = rel_attr_cascade("workout")
