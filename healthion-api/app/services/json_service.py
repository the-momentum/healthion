import json
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from typing import Iterable
from logging import Logger, getLogger

from app.database import DbSession
from app.services.new_workout_service import workout_service
from app.utils.exceptions import handle_exceptions
from app.schemas import (
    # ImportBundle,
    NewRootJSON,
    NewWorkoutJSON,
    QuantityJSON,
    NewWorkoutIn,
    NewWorkoutCreate,
    UploadDataResponse,
)

APPLE_DT_FORMAT = "%Y-%m-%d %H:%M:%S %z"


class JSONService:
    def __init__(self, log: Logger, **kwargs):
        self.log = log
        self.workout_service = workout_service

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

    def _build_import_bundles(self, raw: dict) -> Iterable[NewWorkoutIn]:
        """
        Given the parsed JSON dict from HealthAutoExport, yield ImportBundle(s)
        ready to insert into your ORM session.
        """
        root = NewRootJSON(**raw)
        workouts_raw = root.data.get("workouts", [])
        for w in workouts_raw:
            wjson = NewWorkoutJSON(**w)

            # Always generate a new UUID for workouts to avoid conflicts between users
            wid = uuid4()

            duration = (wjson.endDate - wjson.startDate).total_seconds() / 60

            workout_row = NewWorkoutIn(
                id=wid,
                user_id=wjson.user_id,
                type=wjson.type,
                startDate=wjson.startDate,
                endDate=wjson.endDate,
                duration=Decimal(str(duration)),
                durationUnit="min",
                sourceName=wjson.sourceName,

            )

            yield workout_row

    def load_data(self, db_session: DbSession, raw: dict, user_id: str = None) -> bool:
        for bundle in self._build_import_bundles(raw):
            workout_data = bundle.model_dump()
            if user_id:
                workout_data['user_id'] = UUID(user_id)
            workout_create = NewWorkoutCreate(**workout_data)
            self.workout_service.create(db_session, workout_create)

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


import_service = JSONService(log=getLogger(__name__))
