from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class WorkoutQueryParams(BaseModel):
    """Query parameters for workout filtering and pagination."""

    start_date: Optional[str] = Field(
        None, description="ISO 8601 format (e.g., '2023-12-01T00:00:00Z')"
    )
    end_date: Optional[str] = Field(
        None, description="ISO 8601 format (e.g., '2023-12-31T23:59:59Z')"
    )
    workout_type: Optional[str] = Field(
        None, description="e.g., 'Outdoor Walk', 'Indoor Walk'"
    )
    location: Optional[Literal["Indoor", "Outdoor"]] = Field(
        None, description="Indoor or Outdoor"
    )
    min_duration: Optional[int] = Field(None, description="in seconds")
    max_duration: Optional[int] = Field(None, description="in seconds")
    min_distance: Optional[float] = Field(None, description="in km")
    max_distance: Optional[float] = Field(None, description="in km")
    sort_by: Optional[Literal["date", "duration", "distance", "calories"]] = Field(
        "date", description="Sort field"
    )
    sort_order: Optional[Literal["asc", "desc"]] = Field(
        "desc", description="Sort order"
    )
    limit: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results to return"
    )
    offset: Optional[int] = Field(0, ge=0, description="Number of results to skip")


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
    temperature: Optional[TemperatureValue] = None
    humidity: Optional[HumidityValue] = None
    source: str
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
