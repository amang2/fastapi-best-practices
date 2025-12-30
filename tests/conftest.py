import os
from dotenv import load_dotenv
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.main import app
from src.database.base import Base
from src.database.postgres_conn import get_async_session


load_dotenv(".env.test")
# Test DB URL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
API_BASE_URL = os.getenv("API_BASE_URL")

# -----------------------------
# Test engine and sessionmaker
# -----------------------------
engine_test = create_async_engine(TEST_DATABASE_URL, future=True)
async_session_test = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

# -----------------------------
# Fixture: DB session per test
# -----------------------------
@pytest.fixture
async def db_session():
    """Provide a fresh async session for each test."""
    async with async_session_test() as session:
        async with session.begin():  # start transaction
            yield session
            # rollback happens automatically at end

# -----------------------------
# Override FastAPI dependency
# -----------------------------
async def override_get_test_session():
    # if db_session:
    #     yield db_session
    # else:
    async with async_session_test() as session:
        async with session.begin():
            yield session

# -----------------------------
# AsyncClient fixture
# -----------------------------
@pytest.fixture
async def async_client():
    app.dependency_overrides[get_async_session] = override_get_test_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=API_BASE_URL,
    ) as client:
        yield client

    app.dependency_overrides.clear()

# -----------------------------
# Fixture: Prepare test DB once per session
# -----------------------------
@pytest.fixture(scope="session", autouse=True)
def prepare_test_db():
    sync_engine = create_engine(TEST_DATABASE_URL.replace("+asyncpg", ""))
    Base.metadata.drop_all(bind=sync_engine)
    Base.metadata.create_all(bind=sync_engine)
    yield
    Base.metadata.drop_all(bind=sync_engine)

