import asyncio

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.database import engine, get_async_session
from app.repositories.common import Base

# Database connection string for testing (use a dedicated test database)
# This should ideally be set as an environment variable for better security and flexibility
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost/wardrobers_test"


# --- Pytest Fixtures for Database Session and Clean Up ---
@pytest.fixture(scope="session")
async def async_engine():
    """
    Fixture to create and teardown the database engine.
    Runs once per test session.
    """
    # Use a separate engine for testing to avoid conflicts with the main application
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop existing tables
        await conn.run_sync(Base.metadata.create_all)  # Create tables
    yield test_engine
    await test_engine.dispose()


@pytest.fixture
async def db_session(async_engine) -> AsyncSession:
    """
    Fixture to create and teardown a database session for each test.
    Ensures a clean session for each test, preventing side effects.
    """
    # Use a separate session factory for testing
    TestAsyncSessionLocal = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with TestAsyncSessionLocal() as session:
        yield session
    await session.rollback()


# --- Event Loop Fixture ---
@pytest.fixture(scope="session")
def event_loop():
    """
    Fixture to create an event loop for asynchronous tests.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
