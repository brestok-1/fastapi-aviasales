from typing import Optional

from fastapi_users import schemas

from project.chat.models import Message


class UserRead(schemas.BaseUser[int]):
    id: int

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    id: int
