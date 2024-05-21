import os
import json
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from google.cloud.sql.connector import Connector, IPTypes, create_async_connector


# Get database credentials from the DBCRED environment variable
db_credentials = json.loads(os.environ["DBCRED"])


async def init_connection_pool(connector: Connector) -> AsyncEngine:
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
    async_engine = create_async_engine(
        "postgresql+asyncpg://",
        creator=get_async_conn,
    )
    return async_engine


async def get_async_session():
    # initialize Connector object for connections to Cloud SQL
    connector = await create_async_connector()
    # initialize connection pool
    async_session = await init_connection_pool(connector)
    async with async_session.connect() as session:
        yield session
    # close Connector
    await connector.close_async()
    # dispose of connection pool
    await async_session.dispose()
