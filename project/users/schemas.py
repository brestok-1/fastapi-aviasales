from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    id: int
