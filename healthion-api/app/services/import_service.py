from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID, uuid4
from fastapi import Depends
from typing import Iterable
from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.schemas.health_data import ImportBundle, RootJSON, WorkoutJSON
from app.schemas.health_data import HeartRateDataIn, HeartRateRecoveryIn, ActiveEnergyIn
from app.schemas.health_data import QuantityJSON
from app.schemas.health_data import WorkoutIn
from app.models import Workout, HeartRateData, HeartRateRecovery, ActiveEnergy

APPLE_DT_FORMAT = "%Y-%m-%d %H:%M:%S %z"


class ImportService:
    def __init__(self, db: Session = Depends(get_db)):
        self._db = db

    def _dt(self, s: str) -> datetime:
        s = s.replace(" +", "+").replace(" ", "T", 1)
        if len(s) >= 5 and (s[-5] in {"+", "-"} and s[-3] != ":"):
            s = f"{s[:-2]}:{s[-2:]}"
        return datetime.fromisoformat(s)

    def _dec(self, x: Optional[float | int]) -> Optional[Decimal]:
        return None if x is None else Decimal(str(x))

    def _qty_pair(
        self, q: Optional[QuantityJSON]
    ) -> tuple[Optional[Decimal], Optional[str]]:
        if q is None:
            return None, None
        return self._dec(q.qty), q.units

    def build_import_bundles(self, raw: dict) -> Iterable[ImportBundle]:
        """
        Given the parsed JSON dict from HealthAutoExport, yield ImportBundle(s)
        ready to insert into your ORM session.
        """
        root = RootJSON(**raw)
        workouts_raw = root.data.get("workouts", [])
        for w in workouts_raw:
            wjson = WorkoutJSON(**w)

            try:
                wid = UUID(wjson.id) if wjson.id else uuid4()
            except Exception:
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

            hr_data_rows: List[HeartRateDataIn] = []
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

            hr_recovery_rows: List[HeartRateRecoveryIn] = []
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

            ae_rows: List[ActiveEnergyIn] = []
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

    def load_data(self, raw: dict) -> bool:
        try:
            for bundle in self.build_import_bundles(raw):
                self._db.add(Workout(**bundle.workout.model_dump()))

                for row in bundle.heart_rate_data:
                    self._db.add(HeartRateData(**row.model_dump()))

                for row in bundle.heart_rate_recovery:
                    self._db.add(HeartRateRecovery(**row.model_dump()))

                for row in bundle.active_energy:
                    self._db.add(ActiveEnergy(**row.model_dump()))

            self._db.commit()
        except Exception:
            self._db.rollback()
            raise
        return True
