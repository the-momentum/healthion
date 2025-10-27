from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.apple.common import BaseQueryParams


class WorkoutQueryParams(BaseQueryParams):
    """Query parameters for workout filtering and pagination."""

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
