import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import UUID

from app.models.users.core import (
    User,
    UserInfo,
    UpdateContext,
    RoleAction,
    SubscriptionAction,
)
from app.models.users.roles import Roles
from app.models.authentication import AuthHandler


@pytest.fixture
def test_user(session: AsyncSession):
    """Fixture to create a test user for other tests."""
    user = User(
        login="testuser", password=AuthHandler.get_password_hash("testpassword")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    yield user


@pytest.fixture
def test_role(session: AsyncSession):
    """Fixture to create a test role for other tests."""
    role = Roles(code="admin", name="Administrator")
    session.add(role)
    session.commit()
    session.refresh(role)
    yield role


@pytest.mark.asyncio
async def test_user_creation(session: AsyncSession):
    """Test creating a new user."""
    user = User(login="testuser", password="securepassword")
    session.add(user)
    await session.commit()
    assert user.id is not None


@pytest.mark.asyncio
async def test_user_creation_with_info(session: AsyncSession):
    """Test creating a new user with associated UserInfo."""
    user = User(login="testuser", password="securepassword")
    user.info = UserInfo(
        first_name="Test", last_name="User", email="test@wardrobers.com"
    )
    session.add(user)
    await session.commit()
    assert user.id is not None
    assert user.info.id is not None


@pytest.mark.asyncio
async def test_user_creation_with_duplicate_login(session: AsyncSession):
    """Test preventing duplicate login for User creation."""
    user1 = User(login="testuser", password="securepassword")
    user2 = User(login="testuser", password="securepassword")

    session.add(user1)
    await session.commit()

    session.add(user2)
    with pytest.raises(IntegrityError):
        await session.commit()


@pytest.mark.asyncio
async def test_get_user_by_login(session: AsyncSession):
    """Test retrieving a user by their login."""
    user = User(login="testuser", password="securepassword")
    session.add(user)
    await session.commit()

    retrieved_user = await User.get_user_by_login(session, "testuser")
    assert retrieved_user.id == user.id


@pytest.mark.asyncio
async def test_update_user_info(session: AsyncSession, test_user: User):
    """Test updating user information."""
    await test_user.update_user_info(
        session,
        {"first_name": "Updated", "last_name": "Test"},
        UpdateContext.FULL_PROFILE,
    )
    updated_user = await User.get_by_id(session, test_user.id)
    assert updated_user.info.first_name == "Updated"
    assert updated_user.info.last_name == "Test"


@pytest.mark.asyncio
async def test_manage_roles(session: AsyncSession, test_user: User, test_role: Roles):
    """Test adding and removing roles from a user."""
    # Add role
    await test_user.manage_roles(session, test_role.id, RoleAction.ADD)
    user = await User.get_by_id(session, test_user.id)
    assert test_role in user.roles

    # Remove role
    await test_user.manage_roles(session, test_role.id, RoleAction.REMOVE)
    user = await User.get_by_id(session, test_user.id)
    assert test_role not in user.roles


@pytest.mark.asyncio
async def test_manage_subscription(session: AsyncSession, test_user: User):
    """Test managing user subscriptions."""
    # Add subscription
    await test_user.manage_subscription(
        session,
        {"subscription_type_id": UUID("00000000-0000-0000-0000-000000000001")},
        SubscriptionAction.ADD,
    )
    user = await User.get_by_id(session, test_user.id)
    assert len(user.subscriptions) == 1

    # Update subscription
    await test_user.manage_subscription(
        session,
        {"subscription_type_id": UUID("00000000-0000-0000-0000-000000000002")},
        SubscriptionAction.UPDATE,
    )
    user = await User.get_by_id(session, test_user.id)
    assert user.subscriptions[0].subscription_type_id == UUID(
        "00000000-0000-0000-0000-000000000002"
    )

    # Cancel subscription
    await test_user.manage_subscription(session, {}, SubscriptionAction.CANCEL)
    user = await User.get_by_id(session, test_user.id)
    assert not user.subscriptions[0].is_active


@pytest.mark.asyncio
async def test_toggle_notifications(session: AsyncSession, test_user: User):
    """Test enabling and disabling user notifications."""
    # Enable notifications
    await test_user.toggle_notifications(session, True)
    user = await User.get_by_id(session, test_user.id)
    assert user.is_notificated

    # Disable notifications
    await test_user.toggle_notifications(session, False)
    user = await User.get_by_id(session, test_user.id)
    assert not user.is_notificated


@pytest.mark.asyncio
async def test_validate_password_strength():
    """Test password strength validation."""
    # Valid password
    try:
        User.validate_password_strength("P@ssw0rd123")
    except ValueError:
        pytest.fail("Valid password should not raise an exception.")

    # Invalid passwords
    with pytest.raises(
        ValueError, match="Password must be at least 8 characters long."
    ):
        User.validate_password_strength("Short")
    with pytest.raises(
        ValueError,
        match="Password must include both lowercase and uppercase characters.",
    ):
        User.validate_password_strength("password123")
    with pytest.raises(ValueError, match="Password must include at least one number."):
        User.validate_password_strength("Password!")
    with pytest.raises(
        ValueError, match="Password must include at least one special character."
    ):
        User.validate_password_strength("Password123")


@pytest.mark.asyncio
async def test_confirm_password():
    """Test password confirmation."""
    # Matching passwords
    try:
        await User.confirm_password("Test1234", "Test1234")
    except ValueError:
        pytest.fail("Matching passwords should not raise an exception.")

    # Non-matching passwords
    with pytest.raises(ValueError, match="Passwords do not match."):
        await User.confirm_password("Test1234", "Test12345")


# Add additional test cases for:
# - Soft delete
# - Hard delete
# - Specific use cases for manage_roles, manage_subscription, etc.
