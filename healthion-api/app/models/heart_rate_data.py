from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID as UUIDType

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.workout import Workout


class HeartRateData(Base):
    __tablename__ = "heart_rate_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workout_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE"),
    )
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    source: Mapped[str | None] = mapped_column(Text)
    units: Mapped[str | None] = mapped_column(String(50))
    avg: Mapped[Decimal | None] = mapped_column(Numeric(10, 3))
    min: Mapped[Decimal | None] = mapped_column(Numeric(10, 3))
    max: Mapped[Decimal | None] = mapped_column(Numeric(10, 3))

    workout: Mapped[Workout] = relationship("Workout", back_populates="heart_rate_data")
