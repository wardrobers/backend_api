import os
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from google.cloud.sql.connector import Connector, IPTypes


# Get database credentials from the DBCRED environment variable
db_credentials = json.loads(os.environ["DBCRED"])

# Configure connector
connector = Connector()


async def get_async_conn():
    conn = await connector.connect(
        f"{db_credentials['project']}:{db_credentials['region']}:{db_credentials['instance']}",
        "asyncpg",
        user=db_credentials["user"],
        password=db_credentials["password"],
        db=db_credentials["database"],
        ip_type=IPTypes.PUBLIC,
    )
    return conn


# Create an asynchronous SQLAlchemy engine
async_engine = create_async_engine(
    "postgresql+asyncpg://",
    creator=get_async_conn,
)

# Asynchronous session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
