import pytest


def test_circular_imports():
    """Test for circular imports within the application."""
    try:
        from app import models
        from app import database
        from app import routers
        from app import schemas
        from app import authentication
        from app import services
        assert True
    except ImportError as e:
        pytest.fail(f"Circular import detected: {str(e)}")