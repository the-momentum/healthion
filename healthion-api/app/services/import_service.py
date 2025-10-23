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


    def _convert_old_to_new_format(self, raw: dict) -> tuple[NewWorkoutIn, list[WorkoutStatisticIn]]:
        """
        Convert old format data to new format structure.
        """
        # Always generate a new UUID for workouts to avoid conflicts between users
        wid = uuid4()
        
        # Parse dates
        start_date = self._dt(raw['start'])
        end_date = self._dt(raw['end'])
        
        # Calculate duration in minutes
        duration_minutes = (end_date - start_date).total_seconds() / 60
        
        # Create workout statistics from old format data
        statistics = []
        
        # Active energy burned
        if 'activeEnergyBurned' in raw and raw['activeEnergyBurned']:
            ae_data = raw['activeEnergyBurned']
            statistics.append(WorkoutStatisticIn(
                type="totalEnergyBurned",
                value=ae_data.get('qty', 0),
                unit=ae_data.get('units', 'kcal')
            ))
        
        # Distance (if available)
        if 'distance' in raw and raw['distance']:
            dist_data = raw['distance']
            statistics.append(WorkoutStatisticIn(
                type="totalDistance",
                value=dist_data.get('qty', 0),
                unit=dist_data.get('units', 'm')
            ))
        
        # Intensity (if available)
        if 'intensity' in raw and raw['intensity']:
            intensity_data = raw['intensity']
            statistics.append(WorkoutStatisticIn(
                type="averageIntensity",
                value=intensity_data.get('qty', 0),
                unit=intensity_data.get('units', 'kcal/hr·kg')
            ))
        
        # Temperature (if available)
        if 'temperature' in raw and raw['temperature']:
            temp_data = raw['temperature']
            statistics.append(WorkoutStatisticIn(
                type="environmentalTemperature",
                value=temp_data.get('qty', 0),
                unit=temp_data.get('units', 'degC')
            ))
        
        # Humidity (if available)
        if 'humidity' in raw and raw['humidity']:
            humidity_data = raw['humidity']
            statistics.append(WorkoutStatisticIn(
                type="environmentalHumidity",
                value=humidity_data.get('qty', 0),
                unit=humidity_data.get('units', '%')
            ))
        
        # Use name as workout type, trimmed of spaces
        workout_type = raw.get('name', 'Unknown Workout').strip()
        
        # Create workout data
        workout_data = NewWorkoutIn(
            id=wid,
            type=workout_type,
            startDate=start_date,
            endDate=end_date,
            duration=self._dec(duration_minutes),
            durationUnit="min",
            sourceName=raw.get('name', 'Unknown Workout'),
            workoutStatistics=statistics
        )
        
        return workout_data, statistics

    def _build_new_workout_data(self, raw: dict) -> tuple[NewWorkoutIn, list[WorkoutStatisticIn]]:
        """
        Parse the new JSON format and return workout and statistics data.
        """
        # Parse the new JSON format directly
        workout_json = NewWorkoutJSON(**raw)
        
        # Always generate a new UUID for workouts to avoid conflicts between users
        wid = uuid4()
        
        # Calculate duration in minutes
        duration_minutes = (workout_json.endDate - workout_json.startDate).total_seconds() / 60
        
        workout_data = NewWorkoutIn(
            id=wid,
            type=workout_json.type,
            startDate=workout_json.startDate,
            endDate=workout_json.endDate,
            duration=self._dec(duration_minutes),
            durationUnit="min",
            sourceName=workout_json.sourceName,
            workoutStatistics=workout_json.workoutStatistics or []
        )
        
        return workout_data, workout_json.workoutStatistics or []


    def _is_new_format(self, raw: dict) -> bool:
        """Check if the data is in new format."""
        return all(key in raw for key in ['type', 'startDate', 'endDate', 'sourceName'])

    def load_data(self, db_session: DbSession, raw: dict, user_id: str = None) -> bool:
        # Check format and convert if necessary
        if self._is_new_format(raw):
            # Process new format directly
            workout_data, statistics_data = self._build_new_workout_data(raw)
        else:
            # Convert old format to new format
            workout_data, statistics_data = self._convert_old_to_new_format(raw)
        
        # Create workout
        workout_dict = workout_data.model_dump()
        if user_id:
            workout_dict['user_id'] = UUID(user_id)
        workout_create = NewWorkoutCreate(**workout_dict)
        self.workout_service.create(db_session, workout_create)

        # Create workout statistics
        for stat in statistics_data:
            stat_data = stat.model_dump()
            if user_id:
                stat_data['user_id'] = UUID(user_id)
                stat_data['workout_id'] = workout_data.id
            stat_create = WorkoutStatisticCreate(**stat_data)
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
