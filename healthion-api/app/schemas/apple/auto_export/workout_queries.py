from __future__ import annotations

from typing import Literal

from pydantic import Field

from app.schemas.apple.common import BaseQueryParams


class WorkoutQueryParams(BaseQueryParams):
    """Query parameters for workout filtering and pagination."""

    workout_type: str | None = Field(
        None, description="Workout type (e.g., 'HKWorkoutActivityTypeRunning', 'HKWorkoutActivityTypeWalking')"
    )
    source_name: str | None = Field(
        None, description="Source name of the workout (e.g., 'Apple Watch', 'iPhone')"
    )
    min_duration: int | None = Field(None, description="in seconds")
    max_duration: int | None = Field(None, description="in seconds")
    duration_unit: Literal["s", "min", "h"] | None = Field(
        None, description="Duration unit filter"
    )
    sort_by: Literal["startDate", "endDate", "duration", "type", "sourceName"] | None = Field(
        "startDate", description="Sort field"
    )
