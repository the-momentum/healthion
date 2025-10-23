from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Literal, Any
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.schemas.workout_statistics import WorkoutStatisticIn

class WorkoutResponse(BaseModel):
    """Individual workout response model."""

    id: UUID
    type: str | None = None
    startDate: datetime
    endDate: datetime
    sourceName: str | None = None

# CRUD Schemas
class WorkoutCreate(BaseModel):
    """Schema for creating a workout."""

    id: UUID
    user_id: UUID
    type: str | None = None
    startDate: datetime
    endDate: datetime
    duration: Decimal
    durationUnit: str
    sourceName: str | None = None


class WorkoutUpdate(BaseModel):
    """Schema for updating a workout."""

    type: str | None = None
    startDate: datetime
    endDate: datetime
    sourceName: str | None = None

class WorkoutIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: str | None = None
    type: str | None = None
    startDate: datetime
    endDate: datetime
    duration: Decimal
    durationUnit: str
    sourceName: str | None = None
    workoutStatistics: list[WorkoutStatisticIn] | None = None

class WorkoutJSON(BaseModel):
    id: str | None = None
    user_id: str | None = None
    type: str | None = None
    startDate: datetime
    endDate: datetime
    sourceName: str | None = None
    workoutStatistics: list[WorkoutStatisticIn] | None = None


class RootJSON(BaseModel):
    data: dict[str, Any]
