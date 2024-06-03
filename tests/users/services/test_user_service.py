# tests/users/services/test_user_service.py
from unittest.mock import MagicMock

import pytest
from sqlalchemy.dialects.postgresql import UUID

from app.models.users.core.users_model import UserInfo, Users
from app.services.user_service import UserService


@pytest.fixture
def mock_user_repository():
    """Mock user repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = Users(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        login="testuser",
        is_active=False,
    )
    mock_repo.get_by_id.return_value = Users(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        login="testuser",
        is_active=False,
    )
    mock_repo.get_all.return_value = [
        Users(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            login="testuser",
            is_active=False,
        )
    ]
    mock_repo.get_by_ids.return_value = [
        Users(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            login="testuser",
            is_active=False,
        )
    ]
    mock_repo.update.return_value = Users(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        login="testuser",
        is_active=False,
    )
    mock_repo.soft_delete.return_value = Users(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        login="testuser",
        is_active=False,
    )
    mock_repo.delete.return_value = None
    return mock_repo


@pytest.fixture
def mock_user_info_repository():
    """Mock user info repository for testing."""
    mock_repo = MagicMock()
    mock_repo.create.return_value = UserInfo(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        first_name="Test",
        last_name="Users",
        email="test@wardrobers.com",
    )
    mock_repo.get_by_id.return_value = UserInfo(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        first_name="Test",
        last_name="Users",
        email="test@wardrobers.com",
    )
    return mock_repo


@pytest.fixture
def user_service(mock_user_repository, mock_user_info_repository):
    """Fixture to create a UserService instance for testing."""
    return UserService(
        user_repository=mock_user_repository,
        user_info_repository=mock_user_info_repository,
    )


def test_create_user(user_service):
    """Test creating a new user."""
    user_data = UserCreate(login="testuser", password="securepassword")
    created_user = user_service.create_user(user_data)
    assert created_user.id == UUID("00000000-0000-0000-0000-000000000001")
    assert created_user.login == "testuser"
    user_service.user_repository.create.assert_called_once_with(user_data)


def test_get_user_by_id(user_service):
    """Test retrieving a user by ID."""
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    retrieved_user = user_service.get_user_by_id(user_id)
    assert retrieved_user.id == user_id
    user_service.user_repository.get_by_id.assert_called_once_with(user_id)


def test_get_all_users(user_service):
    """Test retrieving all users."""
    users = user_service.get_all_users()
    assert len(users) == 1
    user_service.user_repository.get_all.assert_called_once()


def test_get_users_by_ids(user_service):
    """Test retrieving users by a list of IDs."""
    user_ids = [UUID("00000000-0000-0000-0000-000000000001")]
    retrieved_users = user_service.get_users_by_ids(user_ids)
    assert len(retrieved_users) == 1
    user_service.user_repository.get_by_ids.assert_called_once_with(user_ids)


def test_update_user(user_service):
    """Test updating a user."""
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    user_update = UserUpdate(login="updateduser")
    updated_user = user_service.update_user(user_id, user_update)
    assert updated_user.id == user_id
    assert updated_user.login == "updateduser"
    user_service.user_repository.update.assert_called_once_with(user_id, user_update)


def test_soft_delete_user(user_service):
    """Test soft deleting a user."""
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    user_service.soft_delete_user(user_id)
    user_service.user_repository.soft_delete.assert_called_once_with(user_id)


def test_delete_user(user_service):
    """Test deleting a user."""
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    user_service.delete_user(user_id)
    user_service.user_repository.delete.assert_called_once_with(user_id)


def test_activate_user(user_service):
    """Test activating a user."""
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    user_service.activate_user(user_id)
    user_service.user_repository.activate_account.assert_called_once_with(user_id)


# Add test cases for other user service methods.
