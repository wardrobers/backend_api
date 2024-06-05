import pytest


def test_circular_imports():
    """Test for circular imports within the application."""
    try:
        from app import database, models, routers, schemas, services, repositories

        assert True
    except ImportError as e:
        pytest.fail(f"Circular import detected: {str(e)}")
