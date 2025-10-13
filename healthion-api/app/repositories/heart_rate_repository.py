from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import and_, desc, func
from sqlalchemy.orm import Query

from app.database import BaseDbModel, DbSession
from app.models.heart_rate_data import HeartRateData
from app.models.heart_rate_recovery import HeartRateRecovery
from app.repositories.repositories import CrudRepository
from app.schemas.heart_rate import HeartRateQueryParams
from app.schemas.heart_rate import (
    HeartRateDataCreate, 
    HeartRateDataUpdate,
    HeartRateRecoveryCreate,
    HeartRateRecoveryUpdate
)


class HeartRateDataRepository(CrudRepository[HeartRateData, HeartRateDataCreate, HeartRateDataUpdate]):
    """Repository for heart rate data database operations."""

    def get_heart_rate_data_with_filters(
        self, 
        db_session: DbSession, 
        query_params: HeartRateQueryParams
    ) -> tuple[list[HeartRateData], int]:
        """
        Get heart rate data with filtering, sorting, and pagination.

        Returns:
            Tuple of (heart_rate_data, total_count)
        """
        query: Query = db_session.query(HeartRateData)

        # Apply filters
        filters = []

        # Date range filters
        if query_params.start_date:
            start_dt = datetime.fromisoformat(
                query_params.start_date.replace("Z", "+00:00")
            )
            filters.append(HeartRateData.date >= start_dt)

        if query_params.end_date:
            end_dt = datetime.fromisoformat(query_params.end_date.replace("Z", "+00:00"))
            filters.append(HeartRateData.date <= end_dt)

        # Workout ID filter
        if query_params.workout_id:
            filters.append(HeartRateData.workout_id == query_params.workout_id)

        # Source filter
        if query_params.source:
            filters.append(HeartRateData.source.ilike(f"%{query_params.source}%"))

        # Heart rate value filters
        if query_params.min_avg is not None:
            filters.append(HeartRateData.avg >= Decimal(str(query_params.min_avg)))

        if query_params.max_avg is not None:
            filters.append(HeartRateData.avg <= Decimal(str(query_params.max_avg)))

        if query_params.min_max is not None:
            filters.append(HeartRateData.max >= Decimal(str(query_params.min_max)))

        if query_params.max_max is not None:
            filters.append(HeartRateData.max <= Decimal(str(query_params.max_max)))

        if query_params.min_min is not None:
            filters.append(HeartRateData.min >= Decimal(str(query_params.min_min)))

        if query_params.max_min is not None:
            filters.append(HeartRateData.min <= Decimal(str(query_params.max_min)))

        # Apply all filters
        if filters:
            query = query.filter(and_(*filters))

        # Get total count before pagination
        total_count = query.count()

        # Apply sorting
        sort_column = getattr(HeartRateData, query_params.sort_by, HeartRateData.date)
        if query_params.sort_order == "asc":
            query = query.order_by(sort_column)
        else:
            query = query.order_by(desc(sort_column))

        # Apply pagination
        query = query.offset(query_params.offset).limit(query_params.limit)

        return query.all(), total_count


class HeartRateRecoveryRepository(CrudRepository[HeartRateRecovery, HeartRateRecoveryCreate, HeartRateRecoveryUpdate]):
    """Repository for heart rate recovery database operations."""

    def get_heart_rate_recovery_with_filters(
        self, 
        db_session: DbSession, 
        query_params: HeartRateQueryParams
    ) -> tuple[list[HeartRateRecovery], int]:
        """
        Get heart rate recovery data with filtering, sorting, and pagination.

        Returns:
            Tuple of (heart_rate_recovery_data, total_count)
        """
        query: Query = db_session.query(HeartRateRecovery)

        # Apply filters
        filters = []

        # Date range filters
        if query_params.start_date:
            start_dt = datetime.fromisoformat(
                query_params.start_date.replace("Z", "+00:00")
            )
            filters.append(HeartRateRecovery.date >= start_dt)

        if query_params.end_date:
            end_dt = datetime.fromisoformat(query_params.end_date.replace("Z", "+00:00"))
            filters.append(HeartRateRecovery.date <= end_dt)

        # Workout ID filter
        if query_params.workout_id:
            filters.append(HeartRateRecovery.workout_id == query_params.workout_id)

        # Source filter
        if query_params.source:
            filters.append(HeartRateRecovery.source.ilike(f"%{query_params.source}%"))

        # Heart rate value filters
        if query_params.min_avg is not None:
            filters.append(HeartRateRecovery.avg >= Decimal(str(query_params.min_avg)))

        if query_params.max_avg is not None:
            filters.append(HeartRateRecovery.avg <= Decimal(str(query_params.max_avg)))

        if query_params.min_max is not None:
            filters.append(HeartRateRecovery.max >= Decimal(str(query_params.min_max)))

        if query_params.max_max is not None:
            filters.append(HeartRateRecovery.max <= Decimal(str(query_params.max_max)))

        if query_params.min_min is not None:
            filters.append(HeartRateRecovery.min >= Decimal(str(query_params.min_min)))

        if query_params.max_min is not None:
            filters.append(HeartRateRecovery.min <= Decimal(str(query_params.max_min)))

        # Apply all filters
        if filters:
            query = query.filter(and_(*filters))

        # Get total count before pagination
        total_count = query.count()

        # Apply sorting
        sort_column = getattr(
            HeartRateRecovery, query_params.sort_by, HeartRateRecovery.date
        )
        if query_params.sort_order == "asc":
            query = query.order_by(sort_column)
        else:
            query = query.order_by(desc(sort_column))

        # Apply pagination
        query = query.offset(query_params.offset).limit(query_params.limit)

        return query.all(), total_count

    def get_heart_rate_summary(
        self, 
        db_session: DbSession, 
        query_params: HeartRateQueryParams
    ) -> dict:
        """
        Get summary statistics for heart rate data.
        """
        # Base query for heart rate data
        hr_query = db_session.query(HeartRateData)
        hr_recovery_query = db_session.query(HeartRateRecovery)

        # Apply same filters as main query
        filters = []
        recovery_filters = []

        # Date range filters
        if query_params.start_date:
            start_dt = datetime.fromisoformat(
                query_params.start_date.replace("Z", "+00:00")
            )
            filters.append(HeartRateData.date >= start_dt)
            recovery_filters.append(HeartRateRecovery.date >= start_dt)

        if query_params.end_date:
            end_dt = datetime.fromisoformat(query_params.end_date.replace("Z", "+00:00"))
            filters.append(HeartRateData.date <= end_dt)
            recovery_filters.append(HeartRateRecovery.date <= end_dt)

        # Workout ID filter
        if query_params.workout_id:
            filters.append(HeartRateData.workout_id == query_params.workout_id)
            recovery_filters.append(HeartRateRecovery.workout_id == query_params.workout_id)

        # Source filter
        if query_params.source:
            filters.append(HeartRateData.source.ilike(f"%{query_params.source}%"))
            recovery_filters.append(
                HeartRateRecovery.source.ilike(f"%{query_params.source}%")
            )

        # Apply filters
        if filters:
            hr_query = hr_query.filter(and_(*filters))
        if recovery_filters:
            hr_recovery_query = hr_recovery_query.filter(and_(*recovery_filters))

        # Get heart rate statistics
        hr_stats = hr_query.with_entities(
            func.count(HeartRateData.id).label("total_records"),
            func.avg(HeartRateData.avg).label("avg_hr"),
            func.max(HeartRateData.max).label("max_hr"),
            func.min(HeartRateData.min).label("min_hr"),
        ).first()

        # Get heart rate recovery statistics
        hr_recovery_stats = hr_recovery_query.with_entities(
            func.avg(HeartRateRecovery.avg).label("avg_recovery"),
            func.max(HeartRateRecovery.max).label("max_recovery"),
            func.min(HeartRateRecovery.min).label("min_recovery"),
        ).first()

        return {
            "total_records": hr_stats.total_records or 0,
            "avg_heart_rate": float(hr_stats.avg_hr or 0),
            "max_heart_rate": float(hr_stats.max_hr or 0),
            "min_heart_rate": float(hr_stats.min_hr or 0),
            "avg_recovery_rate": float(hr_recovery_stats.avg_recovery or 0),
            "max_recovery_rate": float(hr_recovery_stats.max_recovery or 0),
            "min_recovery_rate": float(hr_recovery_stats.min_recovery or 0),
        }
