# tests/users/services/test_user_service.py
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models.users import UserInfo, Users
from app.repositories.users import (
    UserAddressRepository,
    UserInfoRepository,
    UserPhotosRepository,
    UserRoleRepository,
    UsersRepository,
)
from app.schemas.users import (
    UpdateContext,
    UserInfoCreate,
    UserInfoUpdate,
    UsersCreate,
    UsersUpdate,
)
from app.services.users import UsersService


@pytest.fixture
def mock_user_repository():
    """Mock user repository for testing."""
    mock_repo = MagicMock(spec=UsersRepository)
    mock_repo.get_user_by_id.return_value = Users(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        login="testuser",
        password="hashed_password",
        is_notificated=False,
    )
    mock_repo.get_user_by_login.return_value = Users(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        login="testuser",
        password="hashed_password",
        is_notificated=False,
    )
    mock_repo.get_all_users.return_value = [
        Users(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            login="testuser",
            password="hashed_password",
            is_notificated=False,
        )
    ]
    mock_repo.create_user.return_value = Users(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        login="newuser",
        password="hashed_password",
        is_notificated=False,
    )
    mock_repo.update_user.return_value = Users(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        login="updateduser",
        password="hashed_password",
        is_notificated=True,
    )
    mock_repo.delete_user.return_value = None
    mock_repo.toggle_notifications.return_value = None
    return mock_repo


@pytest.fixture
def mock_user_info_repository():
    """Mock user info repository for testing."""
    mock_repo = MagicMock(spec=UserInfoRepository)
    mock_repo.get_user_info_by_user_id.return_value = UserInfo(
        id=UUID("00000000-0000-0000-0000-000000000002"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        first_name="Test",
        last_name="User",
        phone_number="1234567890",
        email="test@example.com",
        lender=False,
    )
    mock_repo.create_user_info.return_value = UserInfo(
        id=UUID("00000000-0000-0000-0000-000000000002"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        first_name="New",
        last_name="User",
        phone_number="9876543210",
        email="newuser@example.com",
        lender=False,
    )
    mock_repo.update_user_info.return_value = UserInfo(
        id=UUID("00000000-0000-0000-0000-000000000002"),
        user_id=UUID("00000000-0000-0000-0000-000000000001"),
        first_name="Updated",
        last_name="User",
        phone_number="1234567890",
        email="updated@example.com",
        lender=True,
    )
    mock_repo.delete_user_info.return_value = None
    return mock_repo


@pytest.fixture
def mock_user_address_repository():
    """Mock user address repository for testing."""
    mock_repo = MagicMock(spec=UserAddressRepository)
    mock_repo.get_addresses_by_user_id.return_value = []
    mock_repo.delete_user_address.return_value = None
    return mock_repo


@pytest.fixture
def mock_user_photo_repository():
    """Mock user photo repository for testing."""
    mock_repo = MagicMock(spec=UserPhotosRepository)
    mock_repo.get_user_photos.return_value = []
    mock_repo.delete_user_photo.return_value = None
    return mock_repo


@pytest.fixture
def mock_user_role_repository():
    """Mock user role repository for testing."""
    mock_repo = MagicMock(spec=UserRoleRepository)
    mock_repo.get_user_roles.return_value = []
    return mock_repo


@pytest.fixture
def user_service(
    mock_user_repository,
    mock_user_info_repository,
    mock_user_address_repository,
    mock_user_photo_repository,
    mock_user_role_repository,
):
    """Fixture to create a UserService instance for testing."""
    return UsersService(
        users_repository=mock_user_repository,
        user_info_repository=mock_user_info_repository,
        user_address_repository=mock_user_address_repository,
        user_photo_repository=mock_user_photo_repository,
        user_role_repository=mock_user_role_repository,
    )


# --- Test Cases ---


@pytest.mark.asyncio
def test_get_user_by_id(user_service: UsersService):
    user = user_service.get_user_by_id(UUID("00000000-0000-0000-0000-000000000001"))
    assert user.id == UUID("00000000-0000-0000-0000-000000000001")
    assert user.login == "testuser"
    user_service.users_repository.get_user_by_id.assert_called_once_with(
        UUID("00000000-0000-0000-0000-000000000001")
    )


@pytest.mark.asyncio
def test_get_user_by_id_not_found(user_service: UsersService):
    user_service.users_repository.get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user_by_id(UUID("00000000-0000-0000-0000-000000000002"))
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
def test_get_user_by_login(user_service: UsersService):
    user = user_service.get_user_by_login("testuser")
    assert user.id == UUID("00000000-0000-0000-0000-000000000001")
    assert user.login == "testuser"
    user_service.users_repository.get_user_by_login.assert_called_once_with("testuser")


@pytest.mark.asyncio
def test_get_user_by_login_not_found(user_service: UsersService):
    user_service.users_repository.get_user_by_login.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user_by_login("nonexistentuser")
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
def test_get_all_users(user_service: UsersService):
    users = user_service.get_all_users()
    assert len(users) == 1
    assert users[0].id == UUID("00000000-0000-0000-0000-000000000001")
    user_service.users_repository.get_all_users.assert_called_once()


@pytest.mark.asyncio
def test_create_user(user_service: UsersService, db_session: Session):
    user_data = UsersCreate(
        login="newuser",
        password="securepassword",
        password_confirmation="securepassword",
    )
    created_user = user_service.create_user(user_data)
    assert created_user.id == UUID("00000000-0000-0000-0000-000000000001")
    assert created_user.login == "newuser"
    user_service.users_repository.create_user.assert_called_once_with(user_data)
    user_service.user_info_repository.create_user_info.assert_called_once_with(
        created_user.id,
        UserInfoCreate(email=user_data.login, first_name="", last_name=""),
    )


@pytest.mark.asyncio
def test_create_user_passwords_dont_match(user_service: UsersService):
    user_data = UsersCreate(
        login="newuser",
        password="securepassword",
        password_confirmation="differentpassword",
    )
    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(user_data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Passwords don't match"


@pytest.mark.asyncio
def test_create_user_login_already_exists(user_service: UsersService):
    user_data = UsersCreate(
        login="testuser",
        password="securepassword",
        password_confirmation="securepassword",
    )
    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(user_data)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Login already in use"


@pytest.mark.asyncio
def test_update_user(user_service: UsersService):
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    user_update = UsersUpdate(login="updateduser", is_notificated=True)
    updated_user = user_service.update_user(
        user_id, user_update, current_user=Users(id=user_id)
    )
    assert updated_user.id == user_id
    assert updated_user.login == "updateduser"
    assert updated_user.is_notificated == True
    user_service.users_repository.update_user.assert_called_once_with(
        user_id, user_update
    )


@pytest.mark.asyncio
def test_update_user_not_found(user_service: UsersService):
    user_id = UUID("00000000-0000-0000-0000-000000000002")
    user_update = UsersUpdate(login="updateduser")
    user_service.users_repository.get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_service.update_user(user_id, user_update, current_user=Users(id=user_id))
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
def test_delete_user(user_service: UsersService):
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    user_service.delete_user(
        user_id, current_user=Users(id=user_id, is_superuser=True)
    )  # Assuming is_superuser for authorization
    user_service.user_address_repository.get_addresses_by_user_id.assert_called_once_with(
        user_id
    )
    user_service.user_photo_repository.get_user_photos.assert_called_once_with(user_id)
    user_service.users_repository.delete_user.assert_called_once_with(user_id)


@pytest.mark.asyncio
def test_delete_user_not_found(user_service: UsersService):
    user_id = UUID("00000000-0000-0000-0000-000000000002")
    user_service.users_repository.get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_service.delete_user(user_id, current_user=Users(id=user_id))
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
def test_update_user_info(user_service: UsersService):
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    user_info_update = UserInfoUpdate(
        first_name="Updated", last_name="User", email="updated@example.com", lender=True
    )
    updated_user_info = user_service.update_user_info(
        user_id, user_info_update, UpdateContext.FULL_PROFILE
    )
    assert updated_user_info.first_name == "Updated"
    assert updated_user_info.lender == True
    user_service.user_info_repository.update_user_info.assert_called_once_with(
        user_id, user_info_update
    )


@pytest.mark.asyncio
def test_update_user_info_not_found(user_service: UsersService):
    user_id = UUID("00000000-0000-0000-0000-000000000002")
    user_info_update = UserInfoUpdate(first_name="Updated")
    user_service.user_info_repository.get_user_info_by_user_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_service.update_user_info(
            user_id, user_info_update, UpdateContext.FULL_PROFILE
        )
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User info not found"


@pytest.mark.asyncio
def test_toggle_notifications(user_service: UsersService):
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    user_service.toggle_notifications(user_id, True, current_user=Users(id=user_id))
    user_service.users_repository.toggle_notifications.assert_called_once_with(
        user_id, True
    )


@pytest.mark.asyncio
def test_toggle_notifications_user_not_found(user_service: UsersService):
    user_id = UUID("00000000-0000-0000-0000-000000000002")
    user_service.users_repository.get_user_by_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        user_service.toggle_notifications(user_id, True, current_user=Users(id=user_id))
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
