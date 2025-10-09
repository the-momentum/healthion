from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class HeartRateQueryParams(BaseModel):
    """Query parameters for heart rate filtering and pagination."""

    start_date: Optional[str] = Field(
        None, description="ISO 8601 format (e.g., '2023-12-01T00:00:00Z')"
    )
    end_date: Optional[str] = Field(
        None, description="ISO 8601 format (e.g., '2023-12-31T23:59:59Z')"
    )
    workout_id: Optional[UUID] = Field(
        None, description="Filter by specific workout ID"
    )
    source: Optional[str] = Field(
        None, description="Filter by data source (e.g., 'Apple Health')"
    )
    min_avg: Optional[float] = Field(None, description="Minimum average heart rate")
    max_avg: Optional[float] = Field(None, description="Maximum average heart rate")
    min_max: Optional[float] = Field(None, description="Minimum maximum heart rate")
    max_max: Optional[float] = Field(None, description="Maximum maximum heart rate")
    min_min: Optional[float] = Field(None, description="Minimum minimum heart rate")
    max_min: Optional[float] = Field(None, description="Maximum minimum heart rate")
    sort_by: Optional[Literal["date", "avg", "max", "min"]] = Field(
        "date", description="Sort field"
    )
    sort_order: Optional[Literal["asc", "desc"]] = Field(
        "desc", description="Sort order"
    )
    limit: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results to return"
    )
    offset: Optional[int] = Field(0, ge=0, description="Number of results to skip")


class HeartRateValue(BaseModel):
    """Heart rate value with unit."""

    value: float
    unit: str = "bpm"


class HeartRateDataResponse(BaseModel):
    """Individual heart rate data response model."""

    id: int
    workout_id: UUID
    date: str  # ISO 8601
    source: Optional[str] = None
    units: Optional[str] = None
    avg: Optional[HeartRateValue] = None
    min: Optional[HeartRateValue] = None
    max: Optional[HeartRateValue] = None


class HeartRateRecoveryResponse(BaseModel):
    """Individual heart rate recovery response model."""

    id: int
    workout_id: UUID
    date: str  # ISO 8601
    source: Optional[str] = None
    units: Optional[str] = None
    avg: Optional[HeartRateValue] = None
    min: Optional[HeartRateValue] = None
    max: Optional[HeartRateValue] = None


class HeartRateSummary(BaseModel):
    """Heart rate summary statistics."""

    total_records: int
    avg_heart_rate: float
    max_heart_rate: float
    min_heart_rate: float
    avg_recovery_rate: float
    max_recovery_rate: float
    min_recovery_rate: float


class HeartRateMeta(BaseModel):
    """Metadata for heart rate response."""

    requested_at: str  # ISO 8601
    filters: dict
    result_count: int
    date_range: dict


class HeartRateListResponse(BaseModel):
    """Response model for heart rate data list endpoint."""

    data: list[HeartRateDataResponse]
    recovery_data: list[HeartRateRecoveryResponse]
    summary: HeartRateSummary
    meta: HeartRateMeta
