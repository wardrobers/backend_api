import asyncio

import pytest
from sqlalchemy.orm import Session, create_async_engine, sessionmaker

from app.database import engine, get_db
from app.repositories.common import Base

# Database connection string for testing (use a dedicated test database)
# This should ideally be set as an environment variable for better security and flexibility
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost/wardrobers_test"


# --- Pytest Fixtures for Database Session and Clean Up ---
@pytest.fixture(scope="session")
def async_engine():
    """
    Fixture to create and teardown the database engine.
    Runs once per test session.
    """
    # Use a separate engine for testing to avoid conflicts with the main application
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    with test_engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)  # Drop existing tables
        conn.run_sync(Base.metadata.create_all)  # Create tables
    yield test_engine
    test_engine.dispose()


@pytest.fixture
def db_session(async_engine) -> Session:
    """
    Fixture to create and teardown a database session for each test.
    Ensures a clean session for each test, preventing side effects.
    """
    # Use a separate session factory for testing
    TestAsyncSessionLocal = sessionmaker(
        bind=async_engine, class_=Session, expire_on_commit=False
    )
    with TestAsyncSessionLocal() as session:
        yield session
    session.rollback()


# --- Event Loop Fixture ---
@pytest.fixture(scope="session")
def event_loop():
    """
    Fixture to create an event loop for asynchronous tests.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
