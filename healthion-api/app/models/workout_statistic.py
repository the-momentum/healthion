from sqlalchemy.orm import Mapped

from app.database import BaseDbModel
from app.mappings import (
    PrimaryKey,
    FKUser,
    ManyToOne,
    datetime_tz,
    numeric_10_2,
    str_10,
    str_50,
)

class WorkoutStatistic(BaseDbModel):
    id: Mapped[PrimaryKey[int]]
    user_id: Mapped[FKUser]

    type: Mapped[str_50]
    startDate: Mapped[datetime_tz]
    endDate: Mapped[datetime_tz]
    sum: Mapped[numeric_10_2 | None]
    average: Mapped[numeric_10_2 | None]
    maximum: Mapped[numeric_10_2 | None]
    minimum: Mapped[numeric_10_2 | None]
    unit: Mapped[str_10]

    user: Mapped[ManyToOne["User"]]
    workout: Mapped[ManyToOne["XMLWorkout"]]