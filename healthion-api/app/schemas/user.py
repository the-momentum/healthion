from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    """User information from authentication."""
    
    user_id: UUID
    auth0_id: str
    email: str
    permissions: list[str]
    payload: dict[str, Any]


class UserResponse(BaseModel):    
    user_id: UUID
    email: str
    permissions: list[str]


class UserCreate(BaseModel):
    auth0_id: str
    email: EmailStr


class UserUpdate(BaseModel):
    email: EmailStr | None = None
