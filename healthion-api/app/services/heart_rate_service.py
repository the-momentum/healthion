from logging import Logger

from app.database import DbSession
from app.models.heart_rate_data import HeartRateData
from app.models.heart_rate_recovery import HeartRateRecovery
from app.repositories.heart_rate_repository import HeartRateDataRepository, HeartRateRecoveryRepository
from app.schemas.heart_rate import HeartRateQueryParams
from app.schemas.heart_rate import (
    HeartRateDataCreate, 
    HeartRateDataUpdate,
    HeartRateRecoveryCreate,
    HeartRateRecoveryUpdate
)
from app.services.services import AppService


class HeartRateDataService(AppService[HeartRateDataRepository, HeartRateData, HeartRateDataCreate, HeartRateDataUpdate]):
    """Service for heart rate data business logic."""

    def __init__(self, log: Logger, **kwargs):
        super().__init__(
            crud_model=HeartRateDataRepository,
            model=HeartRateData,
            log=log,
            **kwargs
        )

    def get_heart_rate_data_with_filters(
        self, 
        db_session: DbSession, 
        query_params: HeartRateQueryParams
    ) -> tuple[list[HeartRateData], int]:
        """
        Get heart rate data with filtering, sorting, and pagination.
        """
        self.logger.info(f"Fetching heart rate data with filters: {query_params.model_dump()}")
        
        data, total_count = self.crud.get_heart_rate_data_with_filters(
            db_session, query_params
        )
        
        self.logger.info(f"Retrieved {len(data)} heart rate records out of {total_count} total")
        
        return data, total_count


class HeartRateRecoveryService(AppService[HeartRateRecoveryRepository, HeartRateRecovery, HeartRateRecoveryCreate, HeartRateRecoveryUpdate]):
    """Service for heart rate recovery business logic."""

    def __init__(self, log: Logger, **kwargs):
        super().__init__(
            crud_model=HeartRateRecoveryRepository,
            model=HeartRateRecovery,
            log=log,
            **kwargs
        )

    def get_heart_rate_recovery_with_filters(
        self, 
        db_session: DbSession, 
        query_params: HeartRateQueryParams
    ) -> tuple[list[HeartRateRecovery], int]:
        """
        Get heart rate recovery data with filtering, sorting, and pagination.
        """
        self.logger.info(f"Fetching heart rate recovery data with filters: {query_params.model_dump()}")
        
        data, total_count = self.crud.get_heart_rate_recovery_with_filters(
            db_session, query_params
        )
        
        self.logger.info(f"Retrieved {len(data)} heart rate recovery records out of {total_count} total")
        
        return data, total_count

    def get_heart_rate_summary(
        self, 
        db_session: DbSession, 
        query_params: HeartRateQueryParams
    ) -> dict:
        """
        Get summary statistics for heart rate data.
        """
        self.logger.info(f"Generating heart rate summary with filters: {query_params.model_dump()}")
        
        summary = self.crud.get_heart_rate_summary(db_session, query_params)
        
        self.logger.info(f"Generated heart rate summary with {summary['total_records']} total records")
        
        return summary


class HeartRateService(HeartRateDataService, HeartRateRecoveryService):
    """
    Combined service for heart rate operations using cooperative inheritance.
    Provides access to both heart rate data and recovery operations.
    """

    def __init__(self, log: Logger, **kwargs):
        # Initialize both parent services
        HeartRateDataService.__init__(self, log=log, **kwargs)
        HeartRateRecoveryService.__init__(self, log=log, **kwargs)

    def get_complete_heart_rate_data(
        self, 
        db_session: DbSession, 
        query_params: HeartRateQueryParams
    ) -> tuple[list[HeartRateData], list[HeartRateRecovery], dict, int, int]:
        """
        Get complete heart rate data including both data and recovery records with summary.
        Uses cooperative inheritance to access both repositories.
        
        Returns:
            Tuple of (heart_rate_data, heart_rate_recovery, summary, hr_total_count, recovery_total_count)
        """
        self.logger.info(f"Fetching complete heart rate data with filters: {query_params.model_dump()}")
        
        # Use cooperative inheritance to call both parent methods
        hr_data, hr_total_count = self.get_heart_rate_data_with_filters(db_session, query_params)
        recovery_data, recovery_total_count = self.get_heart_rate_recovery_with_filters(db_session, query_params)
        summary = self.get_heart_rate_summary(db_session, query_params)
        
        self.logger.info(f"Retrieved complete heart rate data: {hr_total_count} HR records, {recovery_total_count} recovery records")
        
        return hr_data, recovery_data, summary, hr_total_count, recovery_total_count
