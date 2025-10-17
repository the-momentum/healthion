from sqlalchemy.orm import Mapped

from app.database import BaseDbModel
from app.mappings import (
    PrimaryKey,
    FKUser,
    OneToMany,
    ManyToOne,
    datetime_tz,
    numeric_10_2,
    str_10,
    str_100,
    str_50,
)

class XMLWorkout(BaseDbModel):
    id: Mapped[PrimaryKey[int]]
    user_id: Mapped[FKUser]

    type: Mapped[str_50]
    duration: Mapped[numeric_10_2]
    durationUnit: Mapped[str_10]
    sourceName: Mapped[str_100]
    startDate: Mapped[datetime_tz]
    endDate: Mapped[datetime_tz]
    creationDate: Mapped[datetime_tz]

    user: Mapped[ManyToOne["User"]]
    workout_stats: Mapped[OneToMany["WorkoutStatistic"]]