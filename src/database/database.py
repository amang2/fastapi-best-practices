import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


# Read database URL from env var, fallback to a local Postgres example
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/devdatabase")


engine: AsyncEngine = create_async_engine(DATABASE_URL, future=True)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async SQLAlchemy Session for dependency injection."""
    async with async_session_maker() as session:
        yield session


async def init_db():
    """Run initialization tasks such as creating tables.

    Note: This example uses SQLAlchemy's metadata.create_all which is synchronous.
    For full async table creation, import your Base and call run_sync on the engine.
    """
    # If you have declarative Base metadata available import and use it here.
    # Example:
    # from src.user.models import Base
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    pass
