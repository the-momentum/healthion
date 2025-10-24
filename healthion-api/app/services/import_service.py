import json
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4
from typing import Iterable
from logging import Logger, getLogger

from app.database import DbSession
from app.services.new_workout_service import workout_service
from app.services.workout_statistic_service import workout_statistic_service
from app.utils.exceptions import handle_exceptions
from app.schemas import (
    RootJSON,
    NewWorkoutJSON,
    NewWorkoutIn,
    NewWorkoutCreate,
    WorkoutStatisticCreate,
    WorkoutStatisticIn,
    UploadDataResponse,
)

APPLE_DT_FORMAT = "%Y-%m-%d %H:%M:%S %z"


class ImportService:
    def __init__(self, log: Logger, **kwargs):
        self.log = log
        self.workout_service = workout_service
        self.workout_statistic_service = workout_statistic_service

    def _dt(self, s: str) -> datetime:
        s = s.replace(" +", "+").replace(" ", "T", 1)
        if len(s) >= 5 and (s[-5] in {"+", "-"} and s[-3] != ":"):
            s = f"{s[:-2]}:{s[-2:]}"
        return datetime.fromisoformat(s)

    def _dec(self, x: float | int | None) -> Decimal | None:
        return None if x is None else Decimal(str(x))


    def _get_workout_statistics(self, workout: NewWorkoutJSON) -> list[WorkoutStatisticIn]:
        """
        Get workout statistics from workout JSON.
        """
        statistics: list[WorkoutStatisticIn] = []
        
        if 'activeEnergyBurned' in workout and workout['activeEnergyBurned']:
            ae_data = workout['activeEnergyBurned']
            statistics.append(WorkoutStatisticIn(
                type="totalEnergyBurned",
                value=ae_data.get('qty', 0),
                unit=ae_data.get('units', 'kcal')
            ))
        
        if 'distance' in workout and workout['distance']:
            dist_data = workout['distance']
            statistics.append(WorkoutStatisticIn(
                type="totalDistance",
                value=dist_data.get('qty', 0),
                unit=dist_data.get('units', 'm')
            ))
        
        if 'intensity' in workout and workout['intensity']:
            intensity_data = workout['intensity']
            statistics.append(WorkoutStatisticIn(
                type="averageIntensity",
                value=intensity_data.get('qty', 0),
                unit=intensity_data.get('units', 'kcal/hr·kg')
            ))
        
        if 'temperature' in workout and workout['temperature']:
            temp_data = workout['temperature']
            statistics.append(WorkoutStatisticIn(
                type="environmentalTemperature",
                value=temp_data.get('qty', 0),
                unit=temp_data.get('units', 'degC')
            ))
        
        if 'humidity' in workout and workout['humidity']:
            humidity_data = workout['humidity']
            statistics.append(WorkoutStatisticIn(
                type="environmentalHumidity",
                value=humidity_data.get('qty', 0),
                unit=humidity_data.get('units', '%')
            ))

        return statistics
        

    def _build_import_bundles(self, raw: dict) -> Iterable[tuple[NewWorkoutIn, list[WorkoutStatisticIn]]]:
        """
        Given the parsed JSON dict from HealthAutoExport, yield ImportBundles
        ready to insert the database.
        """
        root = RootJSON(**raw)
        workouts_raw = root.data.get("workouts", [])
        
        for w in workouts_raw:
            wjson = NewWorkoutJSON(**w)

            wid = uuid4()

            start_date = self._dt(wjson.startDate)
            end_date = self._dt(wjson.endDate)
            duration = (end_date - start_date).total_seconds() / 60
            duration_unit = "min"

            workout_statistics = self._get_workout_statistics(wjson)

            workout_type = raw.get('name', 'Unknown Workout')

            workout_row = NewWorkoutIn(
                id=wid,
                type=workout_type,
                startDate=start_date,
                endDate=end_date,
                duration=self._dec(duration),
                durationUnit=duration_unit,
                sourceName=wjson.sourceName,
                workoutStatistics=workout_statistics
            )

            

            yield workout_row, workout_statistics


    def load_data(self, db_session: DbSession, raw: dict, user_id: str = None) -> bool:

        for workout_row, workout_statistics in self._build_import_bundles(raw):
            workout_dict = workout_row.model_dump()
            if user_id:
                workout_dict['user_id'] = UUID(user_id)
            workout_create = NewWorkoutCreate(**workout_dict)
            self.workout_service.create(db_session, workout_create)

            for stat in workout_statistics:
                stat_dict = stat.model_dump()
                if user_id:
                    stat_dict['user_id'] = UUID(user_id)
                    stat_dict['workout_id'] = workout_row.id
                stat_create = WorkoutStatisticCreate(**stat_dict)
                self.workout_statistic_service.create(db_session, stat_create)

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
