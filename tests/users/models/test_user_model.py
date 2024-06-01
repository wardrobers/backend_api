import pytest
from uuid import UUID

from app.models.users import User, UserInfo, UpdateContext, Role
from app.database.session import get_session


# Mock Firebase authentication functions
class MockFirebaseAuth:
    def verify_password_reset_token(self, token):
        return "test@example.com"  # Return a test email for verification


@pytest.fixture
def mock_firebase_auth(monkeypatch):
    """Fixture to mock firebase_admin.auth module"""
    monkeypatch.setattr(
        "app.models.users.core.user_model.firebase_auth", MockFirebaseAuth()
    )


@pytest.mark.asyncio
async def test_create_user(mock_firebase_auth):
    """Test creating a new user and activating account"""
    async with get_session() as session:
        user = User(login="testuser", password="securepassword", is_active=False)
        user = await user.create(session)
        assert user.id is not None
        assert not user.is_active

        # Activate the user
        await user.activate_account(session)
        user = await User.get_by_id(session, user.id)
        assert user.is_active


@pytest.mark.asyncio
async def test_get_user_by_login():
    """Test retrieving a user by their login"""
    async with get_session() as session:
        user = User(login="testuser", password="securepassword")
        session.add(user)
        await session.commit()

        retrieved_user = await User.get_user_by_login(session, "testuser")
        assert retrieved_user.id == user.id


@pytest.mark.asyncio
async def test_update_user_info(mock_firebase_auth):
    """Test updating user information"""
    async with get_session() as session:
        user = User(login="testuser", password="securepassword")
        session.add(user)
        await session.commit()

        await user.update_user_info(
            session,
            {"first_name": "Test", "last_name": "User"},
            UpdateContext.FULL_PROFILE,
        )
        updated_user = await User.get_by_id(session, user.id)
        assert updated_user.info.first_name == "Test"
        assert updated_user.info.last_name == "User"


@pytest.mark.asyncio
async def test_manage_roles(mock_firebase_auth):
    """Test adding and removing roles from a user"""
    async with get_session() as session:
        user = User(login="testuser", password="securepassword")
        session.add(user)
        await session.commit()

        role = Role(code="admin", name="Administrator")
        session.add(role)
        await session.commit()

        # Add role
        await user.manage_roles(session, role.id, "add")
        user = await User.get_by_id(session, user.id)
        assert role in user.roles

        # Remove role
        await user.manage_roles(session, role.id, "remove")
        user = await User.get_by_id(session, user.id)
        assert role not in user.roles


@pytest.mark.asyncio
async def test_manage_subscription(mock_firebase_auth):
    """Test managing user subscriptions"""
    async with get_session() as session:
        user = User(login="testuser", password="securepassword")
        session.add(user)
        await session.commit()

        # Add subscription
        await user.manage_subscription(
            session,
            {"subscription_type_id": UUID("00000000-0000-0000-0000-000000000001")},
            "add",
        )
        user = await User.get_by_id(session, user.id)
        assert len(user.subscriptions) == 1

        # Update subscription
        await user.manage_subscription(
            session,
            {"subscription_type_id": UUID("00000000-0000-0000-0000-000000000002")},
            "update",
        )
        user = await User.get_by_id(session, user.id)
        assert user.subscriptions[0].subscription_type_id == UUID(
            "00000000-0000-0000-0000-000000000002"
        )

        # Cancel subscription
        await user.manage_subscription(session, {}, "cancel")
        user = await User.get_by_id(session, user.id)
        assert not user.subscriptions[0].is_active


@pytest.mark.asyncio
async def test_toggle_notifications(mock_firebase_auth):
    """Test enabling and disabling user notifications"""
    async with get_session() as session:
        user = User(login="testuser", password="securepassword")
        session.add(user)
        await session.commit()

        # Enable notifications
        await user.toggle_notifications(session, True)
        user = await User.get_by_id(session, user.id)
        assert user.is_notificated

        # Disable notifications
        await user.toggle_notifications(session, False)
        user = await User.get_by_id(session, user.id)
        assert not user.is_notificated


@pytest.mark.asyncio
async def test_validate_password_strength(mock_firebase_auth):
    """Test password strength validation"""
    async with get_session() as session:
        user = User(login="testuser", password="securepassword")
        session.add(user)
        await session.commit()

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
        with pytest.raises(
            ValueError, match="Password must include at least one number."
        ):
            User.validate_password_strength("Password!")
        with pytest.raises(
            ValueError, match="Password must include at least one special character."
        ):
            User.validate_password_strength("Password123")


@pytest.mark.asyncio
async def test_confirm_password(mock_firebase_auth):
    """Test password confirmation"""
    async with get_session() as session:
        user = User(login="testuser", password="securepassword")
        session.add(user)
        await session.commit()

        # Matching passwords
        try:
            await User.confirm_password("Test1234", "Test1234")
        except ValueError:
            pytest.fail("Matching passwords should not raise an exception.")

        # Non-matching passwords
        with pytest.raises(ValueError, match="Passwords do not match."):
            await User.confirm_password("Test1234", "Test12345")


@pytest.mark.asyncio
async def test_reset_password(mock_firebase_auth):
    """Test password reset with Firebase verification"""
    async with get_session() as session:
        user = User(login="testuser", password="securepassword")
        session.add(user)
        await session.commit()

        # Reset password using mocked Firebase verification
        await user.reset_password(session, "mock_token", "newpassword")
        updated_user = await User.get_by_id(session, user.id)
        assert not User.verify_password("securepassword", updated_user.password)
        assert User.verify_password("newpassword", updated_user.password)


# Test cases for other User model methods can be added here,
# covering functions like soft_delete(), delete(), and more.
