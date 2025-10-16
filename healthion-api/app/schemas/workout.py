from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class WorkoutQueryParams(BaseModel):
    """Query parameters for workout filtering and pagination."""

    start_date: str | None = Field(
        None, description="ISO 8601 format (e.g., '2023-12-01T00:00:00Z')"
    )
    end_date: str | None = Field(
        None, description="ISO 8601 format (e.g., '2023-12-31T23:59:59Z')"
    )
    workout_type: str | None = Field(
        None, description="e.g., 'Outdoor Walk', 'Indoor Walk'"
    )
    location: Literal["Indoor", "Outdoor"] | None = Field(
        None, description="Indoor or Outdoor"
    )
    min_duration: int | None = Field(None, description="in seconds")
    max_duration: int | None = Field(None, description="in seconds")
    min_distance: float | None = Field(None, description="in km")
    max_distance: float | None = Field(None, description="in km")
    sort_by: Literal["date", "duration", "distance", "calories"] | None = Field(
        "date", description="Sort field"
    )
    sort_order: Literal["asc", "desc"] | None = Field(
        "desc", description="Sort order"
    )
    limit: int | None = Field(
        20, ge=1, le=100, description="Number of results to return"
    )
    offset: int | None = Field(0, ge=0, description="Number of results to skip")


class DistanceValue(BaseModel):
    """Distance value with unit."""

    value: float
    unit: str = "km"


class ActiveEnergyValue(BaseModel):
    """Active energy value with unit."""

    value: float
    unit: str = "kJ"


class IntensityValue(BaseModel):
    """Intensity value with unit."""

    value: float
    unit: str = "kcal/hr·kg"


class TemperatureValue(BaseModel):
    """Temperature value with unit."""

    value: float
    unit: str = "degC"


class HumidityValue(BaseModel):
    """Humidity value with unit."""

    value: float
    unit: str = "%"


class WorkoutSummary(BaseModel):
    """Workout summary with heart rate and calorie data."""

    avg_heart_rate: float
    max_heart_rate: float
    min_heart_rate: float
    total_calories: float


class WorkoutResponse(BaseModel):
    """Individual workout response model."""

    id: UUID
    name: str
    location: Literal["Indoor", "Outdoor"]
    start: str  # ISO 8601
    end: str  # ISO 8601
    duration: int  # seconds
    distance: DistanceValue
    active_energy_burned: ActiveEnergyValue
    intensity: IntensityValue
    temperature: TemperatureValue | None = None
    humidity: HumidityValue | None = None
    source: str | None = None
    summary: WorkoutSummary


class DateRange(BaseModel):
    """Date range information."""

    start: str
    end: str
    duration_days: int


class WorkoutMeta(BaseModel):
    """Metadata for workout response."""

    requested_at: str  # ISO 8601
    filters: dict
    result_count: int
    date_range: DateRange


class WorkoutListResponse(BaseModel):
    """Response model for workout list endpoint."""

    data: list[WorkoutResponse]
    meta: WorkoutMeta


# CRUD Schemas
class WorkoutCreate(BaseModel):
    """Schema for creating a workout."""
    
    id: UUID
    user_id: UUID
    name: str | None = None
    location: str | None = None
    start: datetime
    end: datetime
    duration: Decimal | None = None
    active_energy_burned_qty: Decimal | None = None
    active_energy_burned_units: str | None = None
    distance_qty: Decimal | None = None
    distance_units: str | None = None
    intensity_qty: Decimal | None = None
    intensity_units: str | None = None
    humidity_qty: Decimal | None = None
    humidity_units: str | None = None
    temperature_qty: Decimal | None = None
    temperature_units: str | None = None


class WorkoutUpdate(BaseModel):
    """Schema for updating a workout."""
    
    name: str | None = None
    location: str | None = None
    start: datetime | None = None
    end: datetime | None = None
    duration: Decimal | None = None
    active_energy_burned_qty: Decimal | None = None
    active_energy_burned_units: str | None = None
    distance_qty: Decimal | None = None
    distance_units: str | None = None
    intensity_qty: Decimal | None = None
    intensity_units: str | None = None
    humidity_qty: Decimal | None = None
    humidity_units: str | None = None
    temperature_qty: Decimal | None = None
    temperature_units: str | None = None
