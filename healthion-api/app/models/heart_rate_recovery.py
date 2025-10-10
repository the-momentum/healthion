from sqlalchemy.orm import Mapped

from app.database import BaseDbModel
from app.mappings import (
    FKWorkout,
    ManyToOne,
    PrimaryKey,
    datetime_tz,
    numeric_10_3,
    rel_attr,
    str_50,
)


class HeartRateRecovery(BaseDbModel):
    id: Mapped[PrimaryKey[int]]
    workout_id: Mapped[FKWorkout]
    date: Mapped[datetime_tz]
    source: Mapped[str | None]
    units: Mapped[str_50 | None]
    avg: Mapped[numeric_10_3 | None]
    min: Mapped[numeric_10_3 | None]
    max: Mapped[numeric_10_3 | None]

    workout: Mapped[ManyToOne["Workout"]] = rel_attr("heart_rate_recovery")
