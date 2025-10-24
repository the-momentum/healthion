from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict

# Input schemas
class WorkoutStatisticJSON(BaseModel):
    """Schema for parsing WorkoutStatistic from JSON import."""
    type: str
    value: float | int
    unit: str


class WorkoutStatisticCreate(BaseModel):
    """Schema for creating a WorkoutStatistic."""
    user_id: UUID
    workout_id: UUID
    type: str
    value: float | int
    unit: str


class WorkoutStatisticUpdate(BaseModel):
    """Schema for creating a WorkoutStatistic."""
    id: int
    user_id: UUID
    workout_id: UUID
    type: str
    value: float | int
    unit: str


# Output schema
class WorkoutStatisticResponse(BaseModel):
    """Schema for WorkoutStatistic response."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: UUID
    workout_id: UUID
    type: str
    value: float | int
    unit: str


class WorkoutStatisticIn(BaseModel):
    """Schema for workout statistics from JSON input."""
    model_config = ConfigDict(from_attributes=True)

    type: str
    value: float | int
    unit: str