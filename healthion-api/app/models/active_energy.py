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


class ActiveEnergy(Base):
    __tablename__ = "active_energy"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workout_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE"),
    )
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    source: Mapped[str | None] = mapped_column(Text)
    units: Mapped[str | None] = mapped_column(String(50))
    qty: Mapped[Decimal | None] = mapped_column(Numeric(15, 5))

    workout: Mapped[Workout] = relationship("Workout", back_populates="active_energy")
