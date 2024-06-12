import os
from asyncio import current_task
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import create_async_connector


ENV = os.getenv("ENV", default="development")
DATABASE_URL = os.getenv("DATABASE_URL")


def create_connection_string():
    if ENV == "production":
        return (
            f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
            f"@/cloudsql/{os.getenv('CLOUD_SQL_CONNECTION_NAME')}/{os.getenv('DB_NAME')}"
        )
    else:
        return DATABASE_URL


async def get_async_conn():
    """
    Asynchronously creates a database connection using asyncpg.
    Handles both production (Cloud SQL) and development environments.
    """
    if ENV == "production":
        connector = await create_async_connector()
        conn: asyncpg.Connection = await connector.connect_async(
            os.getenv('CLOUD_SQL_CONNECTION_NAME'),
            "asyncpg",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            db=os.getenv("DB_NAME"),
        )
    else:
        conn = await asyncpg.create_pool(dsn=DATABASE_URL)
    return conn


# Create an asynchronous SQLAlchemy engine
engine = create_async_engine(
    create_connection_string(),
    creator=get_async_conn,
    echo=ENV != "production",
)

# Session Factory
async_session_factory = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    async with async_session_factory() as session:
        yield session


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Startup logic here
    # async with engine.begin() as conn:
    #     if ENV in ["development", "local"]:
    #         # Optional: Create database tables in non-production environments
    #         await conn.run_sync(Base.metadata.create_all)
    yield  # The application is now ready to handle requests.
    # Shutdown logic here
    await engine.dispose()
