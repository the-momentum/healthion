from sqlalchemy.orm import Mapped

from app.database import BaseDbModel
from app.mappings import (
    PrimaryKey,
    ManyToOne,
    datetime_tz,
    numeric_10_2,
    str_10,
    str_50,
)

class WorkoutStatistic(BaseDbModel):
    id: Mapped[PrimaryKey[int]]
    type: Mapped[str_50]
    startDate: Mapped[datetime_tz]
    endDate: Mapped[datetime_tz]
    creationDate: Mapped[datetime_tz]
    sum: Mapped[numeric_10_2]
    average: Mapped[numeric_10_2]
    maximum: Mapped[numeric_10_2]
    minimum: Mapped[numeric_10_2]
    unit: Mapped[str_10]

    workout: Mapped[ManyToOne["XMLWorkout"]]