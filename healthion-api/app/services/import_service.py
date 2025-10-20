import json
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from typing import Iterable
from logging import Logger, getLogger

from app.database import DbSession
from app.services.heart_rate_service import heart_rate_service
from app.services.workout_service import workout_service
from app.services.active_energy_service import active_energy_service
from app.utils.exceptions import handle_exceptions
from app.schemas import (
    ImportBundle,
    RootJSON,
    WorkoutJSON,
    HeartRateDataIn,
    HeartRateRecoveryIn,
    ActiveEnergyIn,
    QuantityJSON,
    WorkoutIn,
    WorkoutCreate,
    HeartRateDataCreate,
    HeartRateRecoveryCreate,
    ActiveEnergyCreate,
    UploadDataResponse,
)

APPLE_DT_FORMAT = "%Y-%m-%d %H:%M:%S %z"


class ImportService:
    def __init__(self, log: Logger, **kwargs):
        self.log = log
        self.workout_service = workout_service
        self.heart_rate_data_service = heart_rate_service.heart_rate_data_service
        self.heart_rate_recovery_service = heart_rate_service.heart_rate_recovery_service
        self.active_energy_service = active_energy_service

    def _dt(self, s: str) -> datetime:
        s = s.replace(" +", "+").replace(" ", "T", 1)
        if len(s) >= 5 and (s[-5] in {"+", "-"} and s[-3] != ":"):
            s = f"{s[:-2]}:{s[-2:]}"
        return datetime.fromisoformat(s)

    def _dec(self, x: float | int | None) -> Decimal | None:
        return None if x is None else Decimal(str(x))

    def _qty_pair(
        self, q: QuantityJSON | None
    ) -> tuple[Decimal | None, str | None]:
        if q is None:
            return None, None
        return self._dec(q.qty), q.units

    def _build_import_bundles(self, raw: dict) -> Iterable[ImportBundle]:
        """
        Given the parsed JSON dict from HealthAutoExport, yield ImportBundle(s)
        ready to insert into your ORM session.
        """
        root = RootJSON(**raw)
        workouts_raw = root.data.get("workouts", [])
        for w in workouts_raw:
            wjson = WorkoutJSON(**w)

            # Always generate a new UUID for workouts to avoid conflicts between users
            wid = uuid4()

            active_energy_burned_qty, active_energy_burned_units = self._qty_pair(
                wjson.activeEnergyBurned
            )
            distance_qty, distance_units = self._qty_pair(wjson.distance)
            intensity_qty, intensity_units = self._qty_pair(wjson.intensity)
            humidity_qty, humidity_units = self._qty_pair(wjson.humidity)
            temperature_qty, temperature_units = self._qty_pair(wjson.temperature)

            workout_row = WorkoutIn(
                id=wid,
                name=wjson.name,
                location=wjson.location,
                start=self._dt(wjson.start),
                end=self._dt(wjson.end),
                duration=self._dec(wjson.duration),
                active_energy_burned_qty=active_energy_burned_qty,
                active_energy_burned_units=active_energy_burned_units,
                distance_qty=distance_qty,
                distance_units=distance_units,
                intensity_qty=intensity_qty,
                intensity_units=intensity_units,
                humidity_qty=humidity_qty,
                humidity_units=humidity_units,
                temperature_qty=temperature_qty,
                temperature_units=temperature_units,
            )

            hr_data_rows: list[HeartRateDataIn] = []
            for e in wjson.heartRateData or []:
                hr_data_rows.append(
                    HeartRateDataIn(
                        workout_id=wid,
                        date=self._dt(e.date),
                        source=e.source,
                        units=e.units,
                        avg=self._dec(e.avg),
                        min=self._dec(e.min),
                        max=self._dec(e.max),
                    )
                )

            hr_recovery_rows: list[HeartRateRecoveryIn] = []
            for e in wjson.heartRateRecovery or []:
                hr_recovery_rows.append(
                    HeartRateRecoveryIn(
                        workout_id=wid,
                        date=self._dt(e.date),
                        source=e.source,
                        units=e.units,
                        avg=self._dec(e.avg),
                        min=self._dec(e.min),
                        max=self._dec(e.max),
                    )
                )

            ae_rows: list[ActiveEnergyIn] = []
            for e in wjson.activeEnergy or []:
                ae_rows.append(
                    ActiveEnergyIn(
                        workout_id=wid,
                        date=self._dt(e.date),
                        source=e.source,
                        units=e.units,
                        qty=self._dec(e.qty),
                    )
                )

            yield ImportBundle(
                workout=workout_row,
                heart_rate_data=hr_data_rows,
                heart_rate_recovery=hr_recovery_rows,
                active_energy=ae_rows,
            )

    def load_data(self, db_session: DbSession, raw: dict, user_id: str = None) -> bool:
        for bundle in self._build_import_bundles(raw):
            workout_data = bundle.workout.model_dump()
            if user_id:
                workout_data['user_id'] = UUID(user_id)
            workout_create = WorkoutCreate(**workout_data)
            self.workout_service.create(db_session, workout_create)

            for row in bundle.heart_rate_data:
                hr_data = row.model_dump()
                if user_id:
                    hr_data['user_id'] = UUID(user_id)
                hr_create = HeartRateDataCreate(**hr_data)
                self.heart_rate_data_service.create(db_session, hr_create)

            for row in bundle.heart_rate_recovery:
                hr_recovery_data = row.model_dump()
                if user_id:
                    hr_recovery_data['user_id'] = UUID(user_id)
                hr_recovery_create = HeartRateRecoveryCreate(**hr_recovery_data)
                self.heart_rate_recovery_service.create(db_session, hr_recovery_create)

            for row in bundle.active_energy:
                ae_data = row.model_dump()
                if user_id:
                    ae_data['user_id'] = UUID(user_id)
                ae_create = ActiveEnergyCreate(**ae_data)
                self.active_energy_service.create(db_session, ae_create)

        return True

    @handle_exceptions
    async def import_data_from_request(
        self, 
        db_session: DbSession,
        request_content: str, 
        content_type: str,
        user_id: str
    ) -> UploadDataResponse:
        try:
            # Parse content based on type
            if "multipart/form-data" in content_type:
                data = self._parse_multipart_content(request_content)
            else:
                data = self._parse_json_content(request_content)
            
            if not data:
                return UploadDataResponse(response="No valid data found")
            
            # Load data using provided database session
            self.load_data(db_session, data, user_id=user_id)
                
        except Exception as e:
            return UploadDataResponse(response=f"Import failed: {str(e)}")

        return UploadDataResponse(response="Import successful")

    def _parse_multipart_content(self, content: str) -> dict | None:
        """Parse multipart form data to extract JSON."""            
        json_start = content.find('{\n  "data"')
        if json_start == -1:
            json_start = content.find('{"data"')
        if json_start == -1:
            return None
            
        brace_count = 0
        json_end = json_start
        for i, char in enumerate(content[json_start:], json_start):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_end = i
                    break
        
        if brace_count != 0:
            return None
            
        json_str = content[json_start:json_end + 1]
        return json.loads(json_str)

    def _parse_json_content(self, content: str) -> dict | None:
        """Parse JSON content directly."""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return None


import_service = ImportService(log=getLogger(__name__))
