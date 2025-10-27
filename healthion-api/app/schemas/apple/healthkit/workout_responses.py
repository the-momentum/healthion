from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class WorkoutResponse(BaseModel):
    """Individual workout response model."""

    id: UUID
    type: str | None = None
    startDate: datetime
    endDate: datetime
    sourceName: str | None = None
