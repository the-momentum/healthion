import httpx
from typing import Optional, Literal
from fastmcp import FastMCP

from app.config import settings

workouts_router = FastMCP(name="Workouts MCP")


@workouts_router.tool
async def fetch_workouts(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    workout_type: Optional[str] = None,
    location: Optional[Literal["Indoor", "Outdoor"]] = None,
    min_duration: Optional[int] = None,
    max_duration: Optional[int] = None,
    min_distance: Optional[float] = None,
    max_distance: Optional[float] = None,
    sort_by: Optional[Literal["date", "duration", "distance", "calories"]] = "date",
    sort_order: Optional[Literal["asc", "desc"]] = "desc",
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
) -> dict:
    """
    Fetch workouts with optional filtering, sorting, and pagination.

    Args:
        start_date: Filter by start date (ISO format)
        end_date: Filter by end date (ISO format)
        workout_type: Filter by workout type
        location: Filter by location ('Indoor' or 'Outdoor')
        min_duration: Minimum duration in seconds
        max_duration: Maximum duration in seconds
        min_distance: Minimum distance filter
        max_distance: Maximum distance filter
        sort_by: Sort field ('date', 'duration', 'distance', 'calories')
        sort_order: Sort order ('asc', 'desc')
        limit: Number of records to return (max 100)
        offset: Number of records to skip

    Returns:
        Workout data with metadata
    """
    if not settings.healthion_api_access_token:
        raise ValueError("HEALTHION_API_ACCESS_TOKEN environment variable is required")

    base_url = settings.healthion_api_base_url.rstrip("/")
    url = f"{base_url}/api/v1/workouts"

    params = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if workout_type:
        params["workout_type"] = workout_type
    if location:
        params["location"] = location
    if min_duration is not None:
        params["min_duration"] = min_duration
    if max_duration is not None:
        params["max_duration"] = max_duration
    if min_distance is not None:
        params["min_distance"] = min_distance
    if max_distance is not None:
        params["max_distance"] = max_distance
    if sort_by:
        params["sort_by"] = sort_by
    if sort_order:
        params["sort_order"] = sort_order
    if limit is not None:
        params["limit"] = min(limit, 100)  # Enforce max limit
    if offset is not None:
        params["offset"] = offset

    headers = {
        "Authorization": f"Bearer {settings.healthion_api_access_token.get_secret_value()}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
