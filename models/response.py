from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime = None
    is_active: bool
    created_by: str = ''


class UsersResponse(BaseModel):
    __root__: List[UserResponse] = None


class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str
