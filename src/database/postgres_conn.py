import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config.config import DATABASE_URL



engine: AsyncEngine = create_async_engine(DATABASE_URL, future=True)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async SQLAlchemy Session for dependency injection."""
    async with async_session_maker() as session:
        async with session.begin():
            yield session