import httpx
from typing import Optional, Literal
from fastmcp import FastMCP

from app.config import settings

heart_rate_router = FastMCP(name="Heart Rate MCP")


@heart_rate_router.tool
async def fetch_heart_rates(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    workout_id: Optional[str] = None,
    source: Optional[str] = None,
    min_avg: Optional[float] = None,
    max_avg: Optional[float] = None,
    min_max: Optional[float] = None,
    max_max: Optional[float] = None,
    min_min: Optional[float] = None,
    max_min: Optional[float] = None,
    sort_by: Optional[Literal["date", "avg", "max", "min"]] = "date",
    sort_order: Optional[Literal["asc", "desc"]] = "desc",
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
) -> dict:
    """
    Fetch heart rate data with optional filtering, sorting, and pagination.

    Args:
        start_date: Filter by start date (ISO format)
        end_date: Filter by end date (ISO format)
        workout_id: Filter by workout UUID
        source: Filter by data source
        min_avg: Minimum average heart rate filter (float)
        max_avg: Maximum average heart rate filter (float)
        min_max: Minimum max heart rate filter (float)
        max_max: Maximum max heart rate filter (float)
        min_min: Minimum min heart rate filter (float)
        max_min: Maximum min heart rate filter (float)
        sort_by: Sort field ('date', 'avg', 'max', 'min')
        sort_order: Sort order ('asc', 'desc')
        limit: Number of records to return (integer, max 100, default: 20)
        offset: Number of records to skip (integer, default: 0)

    Returns:
        Heart rate data with summary and metadata
    """
    if not settings.healthion_api_access_token:
        raise ValueError("HEALTHION_API_ACCESS_TOKEN environment variable is required")

    base_url = settings.healthion_api_base_url.rstrip("/")
    url = f"{base_url}/api/v1/heart-rate"

    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if workout_id:
        params["workout_id"] = workout_id
    if source:
        params["source"] = source
    if min_avg is not None:
        params["min_avg"] = float(min_avg) if isinstance(min_avg, str) else min_avg
    if max_avg is not None:
        params["max_avg"] = float(max_avg) if isinstance(max_avg, str) else max_avg
    if min_max is not None:
        params["min_max"] = float(min_max) if isinstance(min_max, str) else min_max
    if max_max is not None:
        params["max_max"] = float(max_max) if isinstance(max_max, str) else max_max
    if min_min is not None:
        params["min_min"] = float(min_min) if isinstance(min_min, str) else min_min
    if max_min is not None:
        params["max_min"] = float(max_min) if isinstance(max_min, str) else max_min
    if sort_by:
        params["sort_by"] = sort_by
    if sort_order:
        params["sort_order"] = sort_order
    if limit is not None:
        limit_val = int(limit) if isinstance(limit, str) else limit
        params["limit"] = min(limit_val, 100)  # Enforce max limit
    if offset is not None:
        params["offset"] = int(offset) if isinstance(offset, str) else offset

    headers = {
        "Authorization": f"Bearer {settings.healthion_api_access_token.get_secret_value()}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
