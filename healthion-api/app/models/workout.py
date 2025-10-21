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
    str_10,
    str_100,
    str_50,
)


class Workout(BaseDbModel):
    id: Mapped[PrimaryKey[UUID]]
    user_id: Mapped[FKUser]

    type: Mapped[str_50]
    duration: Mapped[numeric_10_2]
    durationUnit: Mapped[str_10]  # albo całe duration jako string?
    sourceName: Mapped[str_100]

    startDate: Mapped[datetime_tz]
    endDate: Mapped[datetime_tz]

    user: Mapped[ManyToOne["User"]]

    # np. active_energy, heart_rate_data
    workout_statistics: Mapped[OneToMany["WorkoutStatistic"]]

    # workout_entries: Mapped[OneToMany["WorkoutEntry"]] ??
    # workout_routes: Mapped[OneToMany["WorkoutRoute"]] ??
