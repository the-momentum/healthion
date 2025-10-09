from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Any, Optional, List, Dict

from pydantic import BaseModel, Field, ConfigDict, field_validator


class WorkoutIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: Optional[str] = None
    location: Optional[str] = None
    start: datetime
    end: datetime
    duration: Optional[Decimal] = None

    active_energy_burned_qty: Optional[Decimal] = None
    active_energy_burned_units: Optional[str] = None
    distance_qty: Optional[Decimal] = None
    distance_units: Optional[str] = None
    intensity_qty: Optional[Decimal] = None
    intensity_units: Optional[str] = None
    humidity_qty: Optional[Decimal] = None
    humidity_units: Optional[str] = None
    temperature_qty: Optional[Decimal] = None
    temperature_units: Optional[str] = None


class HeartRateDataIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workout_id: UUID
    date: datetime
    source: Optional[str] = None
    units: Optional[str] = None
    avg: Optional[Decimal] = None
    min: Optional[Decimal] = None
    max: Optional[Decimal] = None


class HeartRateRecoveryIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workout_id: UUID
    date: datetime
    source: Optional[str] = None
    units: Optional[str] = None
    avg: Optional[Decimal] = None
    min: Optional[Decimal] = None
    max: Optional[Decimal] = None


class ActiveEnergyIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workout_id: UUID
    date: datetime
    source: Optional[str] = None
    units: Optional[str] = None
    qty: Optional[Decimal] = None


class QuantityJSON(BaseModel):
    qty: Optional[float | int] = None
    units: Optional[str] = None


class HeartRateEntryJSON(BaseModel):
    avg: Optional[float] = Field(default=None, alias="Avg")
    min: Optional[float] = Field(default=None, alias="Min")
    max: Optional[float] = Field(default=None, alias="Max")
    units: Optional[str] = None
    date: str
    source: Optional[str] = None

    @field_validator("date")
    @classmethod
    def parse_date(cls, v: str) -> str:
        return v


class ActiveEnergyEntryJSON(BaseModel):
    qty: Optional[float | int] = None
    units: Optional[str] = None
    date: str
    source: Optional[str] = None


class WorkoutJSON(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    start: str
    end: str
    duration: Optional[float] = None

    activeEnergyBurned: Optional[QuantityJSON] = None
    distance: Optional[QuantityJSON] = None
    intensity: Optional[QuantityJSON] = None
    humidity: Optional[QuantityJSON] = None
    temperature: Optional[QuantityJSON] = None

    heartRateData: Optional[List[HeartRateEntryJSON]] = None
    heartRateRecovery: Optional[List[HeartRateEntryJSON]] = None
    activeEnergy: Optional[List[ActiveEnergyEntryJSON]] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)


class RootJSON(BaseModel):
    data: Dict[str, Any]


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
    heart_rate_data: List[HeartRateDataIn] = []
    heart_rate_recovery: List[HeartRateRecoveryIn] = []
    active_energy: List[ActiveEnergyIn] = []
