from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from project.config import settings

Base = declarative_base()


def get_async_engine(url: str) -> AsyncEngine:
    # Создаем объект AsyncEngine
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


def get_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    # Создаем объект async_sessionmaker
    return async_sessionmaker(bind=engine, class_=AsyncSession)


engine = get_async_engine(
    settings.DATABASE_URL
)
async_session_maker = get_async_sessionmaker(engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    # Генератор, который возвращает объект AsyncSession
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    from project.users.models import User
    # Получаем объект пользователя
    yield SQLAlchemyUserDatabase(session, User)
