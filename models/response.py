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


class BookLink(BaseModel):
    id: int
    name: str


class Book(BookLink):
    description: str = ''
    added_at: datetime = None


class Books(BaseModel):
    user_id: int
    user_name: str
    books: List[Book]
    page_size: int = 10
    page_number: int = 0


class LinkBooksForUser(BaseModel):
    user_id: int
    book_ids: List[BookLink]
