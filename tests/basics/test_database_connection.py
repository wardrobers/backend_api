import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_async_session, engine


@pytest.mark.asyncio
async def test_database_connection():
    """Test if a connection to the database can be established."""
    try:
        async with get_async_session() as session:
            await session.execute("SELECT 1")
        assert True
    except Exception as e:
        pytest.fail(f"Failed to connect to the database: {str(e)}")
