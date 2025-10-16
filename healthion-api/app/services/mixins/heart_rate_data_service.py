from logging import Logger

from app.database import DbSession
from app.models import HeartRateData
from app.repositories import HeartRateDataRepository
from app.schemas import (
    HeartRateQueryParams,
    HeartRateDataCreate, 
    HeartRateDataUpdate
)
from app.services import AppService
from app.utils.exceptions import handle_exceptions


class HeartRateDataService(AppService[HeartRateDataRepository, HeartRateData, HeartRateDataCreate, HeartRateDataUpdate]):
    """Service for heart rate data business logic."""

    def __init__(self, log: Logger, **kwargs):
        super().__init__(
            crud_model=HeartRateDataRepository,
            model=HeartRateData,
            log=log,
            **kwargs
        )

    @handle_exceptions
    async def get_heart_rate_data_with_filters(
        self, 
        db_session: DbSession, 
        query_params: HeartRateQueryParams,
        user_id: str
    ) -> tuple[list[HeartRateData], int]:
        """
        Get heart rate data with filtering, sorting, and pagination.
        """
        self.logger.info(f"Fetching heart rate data with filters: {query_params.model_dump()}")
        
        data, total_count = self.crud.get_heart_rate_data_with_filters(
            db_session, query_params, user_id
        )
        
        self.logger.info(f"Retrieved {len(data)} heart rate records out of {total_count} total")
        
        return data, total_count
