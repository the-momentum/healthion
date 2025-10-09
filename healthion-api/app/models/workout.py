from datetime import datetime
from decimal import Decimal
from uuid import UUID as UUIDType

from sqlalchemy import (
    DateTime,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str | None] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(100))
    start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    duration: Mapped[Decimal | None] = mapped_column(Numeric(15, 5))

    # aggregate metrics
    active_energy_burned_qty: Mapped[Decimal | None] = mapped_column(Numeric(15, 5))
    active_energy_burned_units: Mapped[str | None] = mapped_column(String(50))
    distance_qty: Mapped[Decimal | None] = mapped_column(Numeric(15, 5))
    distance_units: Mapped[str | None] = mapped_column(String(50))
    intensity_qty: Mapped[Decimal | None] = mapped_column(Numeric(15, 5))
    intensity_units: Mapped[str | None] = mapped_column(String(50))
    humidity_qty: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    humidity_units: Mapped[str | None] = mapped_column(String(10))
    temperature_qty: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    temperature_units: Mapped[str | None] = mapped_column(String(10))

    # relationships
    heart_rate_data: Mapped[list["HeartRateData"]] = relationship(
        back_populates="workout",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    heart_rate_recovery: Mapped[list["HeartRateRecovery"]] = relationship(
        back_populates="workout",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    active_energy: Mapped[list["ActiveEnergy"]] = relationship(
        back_populates="workout",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
