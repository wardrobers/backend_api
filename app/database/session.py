import os
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.common import Base

ENV = os.getenv("ENV", default="development")
DATABASE_URL = os.getenv("DATABASE_URL")

def create_connection_string():
    if ENV == "production":
        return (
            f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
            f"@/cloudsql/{os.getenv('CLOUD_SQL_CONNECTION_NAME')}/{os.getenv('DB_NAME')}"
        )
    else:
        return f"postgresql+asyncpg://{DATABASE_URL}"

async def get_async_conn():
    if ENV == "production":
        conn = await asyncpg.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME"),
            host=f"/cloudsql/{os.getenv('CLOUD_SQL_CONNECTION_NAME')}"
        )
    else:
        conn = await asyncpg.connect(dsn=DATABASE_URL)
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
    async with engine.begin() as conn:
        if ENV in ["development", "local"]:
            # Optional: Create database tables in non-production environments
            await conn.run_sync(Base.metadata.create_all)
        pass
    yield  # The application is now ready to handle requests.
    # Shutdown logic here
    await engine.dispose()
