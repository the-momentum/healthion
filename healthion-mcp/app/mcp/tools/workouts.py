import httpx
from typing import Optional, Literal

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token

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
        min_duration: Minimum duration in seconds (integer)
        max_duration: Maximum duration in seconds (integer)
        min_distance: Minimum distance filter (float)
        max_distance: Maximum distance filter (float)
        sort_by: Sort field ('date', 'duration', 'distance', 'calories')
        sort_order: Sort order ('asc', 'desc')
        limit: Number of records to return (integer, max 100, default: 20)
        offset: Number of records to skip (integer, default: 0)

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
        params["min_duration"] = int(min_duration) if isinstance(min_duration, str) else min_duration
    if max_duration is not None:
        params["max_duration"] = int(max_duration) if isinstance(max_duration, str) else max_duration
    if min_distance is not None:
        params["min_distance"] = float(min_distance) if isinstance(min_distance, str) else min_distance
    if max_distance is not None:
        params["max_distance"] = float(max_distance) if isinstance(max_distance, str) else max_distance
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
        # "Authorization": f"Bearer {settings.healthion_api_access_token.get_secret_value()}",
        "Content-Type": "application/json",
    }

    token = get_access_token()
    if not token:
        raise ValueError("No access token found")
    headers["Authorization"] = f"Bearer {token.token}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
