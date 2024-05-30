import os
import json
import asyncpg
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes, create_async_connector


# Get database credentials from the DBCRED environment variable
db_credentials = json.loads(os.environ["DBCRED"])
connector = Connector()


# initialize Connector object for connections to Cloud SQL
async def get_async_conn() -> asyncpg.Connection:
    conn: asyncpg.Connection = await connector.connect_async(
        f"{db_credentials['project']}:{db_credentials['region']}:{db_credentials['instance']}",
        "asyncpg",
        user=db_credentials["user"],
        password=db_credentials["password"],
        db=db_credentials["database"],
        ip_type=IPTypes.PUBLIC,
    )
    return conn


# Create an asynchronous SQLAlchemy engine
engine = create_async_engine(
    "postgresql+asyncpg://",
    creator=get_async_conn,
    echo=True,  # Set to False in production
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
