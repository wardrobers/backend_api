import os
from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

ENV = os.getenv("ENV", default="development")

if ENV == "production":
    echo = False

    async def get_async_conn() -> asyncpg.Connection:
        # Construct connection string for production using environment variables
        connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASS")
        db_name = os.getenv("DB_NAME")
        return f"postgresql+asyncpg://{db_user}:{db_pass}@/{db_name}?host=/cloudsql/{connection_name}"

else:
    echo = True

    async def get_async_conn() -> asyncpg.Connection:
        return await asyncpg.connect(dsn=os.environ["DATABASE_URL"])


# Create an asynchronous SQLAlchemy engine
engine = create_async_engine(
    "postgresql+asyncpg://",
    creator=get_async_conn,
    echo=echo,  # Set to False in production
)

# Session Factory
async_session_factory = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Startup logic here
    async with engine.begin() as conn:
        # Optional: Create database tables
        # await conn.run_sync(Base.metadata.create_all)
        pass
    yield  # The application is now ready to handle requests.
    # Shutdown logic here
    await engine.dispose()
