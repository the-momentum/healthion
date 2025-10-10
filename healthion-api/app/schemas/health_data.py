from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Any

from pydantic import BaseModel, Field, ConfigDict, field_validator


class WorkoutIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
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


class HeartRateDataIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workout_id: UUID
    date: datetime
    source: str | None = None
    units: str | None = None
    avg: Decimal | None = None
    min: Decimal | None = None
    max: Decimal | None = None


class HeartRateRecoveryIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workout_id: UUID
    date: datetime
    source: str | None = None
    units: str | None = None
    avg: Decimal | None = None
    min: Decimal | None = None
    max: Decimal | None = None


class ActiveEnergyIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workout_id: UUID
    date: datetime
    source: str | None = None
    units: str | None = None
    qty: Decimal | None = None


class QuantityJSON(BaseModel):
    qty: float | int | None = None
    units: str | None = None


class HeartRateEntryJSON(BaseModel):
    avg: float | None = Field(default=None, alias="Avg")
    min: float | None = Field(default=None, alias="Min")
    max: float | None = Field(default=None, alias="Max")
    units: str | None = None
    date: str
    source: str | None = None

    @field_validator("date")
    @classmethod
    def parse_date(cls, v: str) -> str:
        return v


class ActiveEnergyEntryJSON(BaseModel):
    qty: float | int | None = None
    units: str | None = None
    date: str
    source: str | None = None


class WorkoutJSON(BaseModel):
    id: str | None = None
    name: str | None = None
    location: str | None = None
    start: str
    end: str
    duration: float | None = None

    activeEnergyBurned: QuantityJSON | None = None
    distance: QuantityJSON | None = None
    intensity: QuantityJSON | None = None
    humidity: QuantityJSON | None = None
    temperature: QuantityJSON | None = None

    heartRateData: list[HeartRateEntryJSON] | None = None
    heartRateRecovery: list[HeartRateEntryJSON] | None = None
    activeEnergy: list[ActiveEnergyEntryJSON] | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class RootJSON(BaseModel):
    data: dict[str, Any]


class ImportBundle(BaseModel):
    """
    Container returned by the factory:
    - workout: WorkoutIn
    - heart_rate_data: list[HeartRateDataIn]
    - heart_rate_recovery: list[HeartRateRecoveryIn]
    - active_energy: list[ActiveEnergyIn]
    """

    model_config = ConfigDict(from_attributes=True)

    workout: WorkoutIn
    heart_rate_data: list[HeartRateDataIn] = []
    heart_rate_recovery: list[HeartRateRecoveryIn] = []
    active_energy: list[ActiveEnergyIn] = []
