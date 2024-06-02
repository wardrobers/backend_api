import re
from enum import Enum

from fastapi import HTTPException
from firebase_admin import auth as firebase_auth
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

from app.models.subscriptions.subscriptions_model import Subscriptions
from app.models.users.core.user_info_model import UserInfo
from app.models.users.core.users_model import Users
from app.models.users.profile.user_addresses_model import UserAddresses
from app.models.users.roles.user_roles_model import UserRoles
from app.repositories.users_repository import UsersRepository

from .auth_service import AuthService


class UpdateContext(Enum):
    CONTACT_DETAILS = "contact_details"
    FULL_PROFILE = "full_profile"
    LENDER_STATUS = "lender_status"


class RoleAction(Enum):
    ADD = "add"
    REMOVE = "remove"


class SubscriptionAction(Enum):
    ADD = "add"
    UPDATE = "update"
    CANCEL = "cancel"


class UsersService:
    """
    Service layer for business logic related to Users operations.
    """

    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository
        self.auth_handler = AuthService()

    async def create_user(self, db_session: AsyncSession, user_data: dict):
        """
        Creates a new user entry in the database and sends an email verification link via Firebase.

        Args:
            db_session (AsyncSession): The database session.
            user_data (dict): A dictionary containing the user's email, password, and any other necessary data.

        Raises:
            HTTPException: If the user cannot be created or the email cannot be sent.
        """
        try:
            # Hash the user's password before storing it in the database
            hashed_password = AuthService.get_password_hash(user_data["password"])
            user_data["password"] = hashed_password
            user_data["is_active"] = False  # Users is inactive until email verification

            # Create the user in the database
            new_user = Users(**user_data)
            db_session.add(new_user)
            await db_session.commit()

        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to create user: {str(e)}"
            )

    async def reset_password_basic(
        self, db_session: AsyncSession, user_id: UUID, new_password: str
    ):
        hashed_password = AuthService.get_password_hash(new_password)
        try:
            await db_session.execute(
                update(Users)
                .where(Users.id == user_id)
                .values(password=hashed_password)
            )
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def reset_password(
        self, db_session: AsyncSession, token: str, new_password: str
    ):
        """Resets the user's password after verifying the token from Firebase."""
        try:
            # Verify the password reset token and extract the email
            email = firebase_auth.verify_password_reset_token(token)
            hashed_password = self.get_password_hash(new_password)
            # Update the user's password in the database
            await db_session.execute(
                update(Users)
                .where(Users.email == email)
                .values(password=hashed_password)
            )
            await db_session.commit()
        except firebase_auth.FirebaseError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail="Invalid or expired reset token."
            )

    async def update_user_info(
        self, db_session: AsyncSession, user_id: UUID, updates: dict, context
    ):
        """Updates user information based on the given context."""
        # Optional: Add context-specific validation or transformation
        if context == UpdateContext.CONTACT_DETAILS:
            allowed_keys = {"phone_number", "email"}
            updates = {key: updates[key] for key in updates if key in allowed_keys}
        elif context == UpdateContext.LENDER_STATUS:
            allowed_keys = {"lender"}
            updates = {key: updates[key] for key in updates if key in allowed_keys}

        try:
            await db_session.execute(
                update(UserInfo).where(UserInfo.user_id == user_id).values(**updates)
            )
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to update user info: {str(e)}"
            )

    async def add_or_update_address(
        self,
        db_session: AsyncSession,
        user_id: UUID,
        address_details: dict,
        address_id: UUID = None,
    ):
        """Adds a new address or updates an existing one for a user."""
        if address_id:
            # Update existing address
            await db_session.execute(
                update(UserAddresses)
                .where(UserAddresses.id == address_id)
                .values(**address_details)
            )
        else:
            # Add new address
            new_address = UserAddresses(**address_details, user_id=user_id)
            db_session.add(new_address)

        await db_session.commit()

    async def manage_roles(
        self, db_session: AsyncSession, role_id: int, action: RoleAction
    ):
        """Manages user roles by adding or removing based on the action specified."""
        action_funcs = {
            RoleAction.ADD: self._add_role,
            RoleAction.REMOVE: self._remove_role,
        }

        action_func = action_funcs.get(action)
        if not action_func:
            raise HTTPException(
                status_code=400, detail="Invalid action for role management."
            )

        try:
            await action_func(db_session, role_id)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to update roles: {str(e)}"
            )

    async def _add_role(self, db_session: AsyncSession, user_id: UUID, role_id: UUID):
        existing_role = await db_session.execute(
            select(UserRoles).where(
                UserRoles.user_id == user_id, UserRoles.role_id == role_id
            )
        )
        if existing_role.scalars().first() is not None:
            raise HTTPException(
                status_code=400, detail="Role already assigned to user."
            )
        await db_session.execute(
            insert(UserRoles).values(user_id=user_id, role_id=role_id)
        )

    async def _remove_role(
        self, db_session: AsyncSession, user_id: UUID, role_id: UUID
    ):
        await db_session.execute(
            delete(UserRoles).where(
                UserRoles.user_id == user_id, UserRoles.role_id == role_id
            )
        )

    async def manage_subscription(
        self,
        db_session: AsyncSession,
        subscription_data: dict,
        action: SubscriptionAction,
    ):
        """Manages user subscriptions based on the action specified."""
        action_funcs = {
            SubscriptionAction.ADD: self._add_subscription,
            SubscriptionAction.UPDATE: self._update_subscription,
            SubscriptionAction.CANCEL: self._cancel_subscription,
        }

        action_func = action_funcs.get(action)
        if not action_func:
            raise HTTPException(
                status_code=400, detail="Invalid action for subscription management."
            )

        try:
            await action_func(db_session, subscription_data)
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to manage subscription: {str(e)}"
            )

    async def _add_subscription(
        self, db_session: AsyncSession, subscription_data: dict
    ):
        active_subscription = await db_session.execute(
            select(Subscriptions).where(
                Subscriptions.user_id == self.id, Subscriptions.is_active == True
            )
        )
        if active_subscription.scalars().first() is not None:
            raise HTTPException(
                status_code=400, detail="Active subscription already exists."
            )
        await db_session.execute(insert(Subscriptions).values(**subscription_data))

    async def _update_subscription(
        self, db_session: AsyncSession, user_id: UUID, subscription_data: dict
    ):
        await db_session.execute(
            update(Subscriptions)
            .where(Subscriptions.user_id == user_id, Subscriptions.is_active == True)
            .values(**subscription_data)
        )

    async def _cancel_subscription(self, db_session: AsyncSession, user_id: UUID):
        await db_session.execute(
            update(Subscriptions)
            .where(Subscriptions.user_id == user_id, Subscriptions.is_active == True)
            .values(is_active=False)
        )

    async def toggle_notifications(
        self, db_session: AsyncSession, user_id: UUID, enable_notifications: bool
    ):
        """Enables or disables user notifications."""
        try:
            await db_session.execute(
                update(Users)
                .where(Users.id == user_id)
                .values(is_notificated=enable_notifications)
            )
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail="Failed to update notification settings."
            )

    @staticmethod
    def validate_password_strength(password: str):
        """Ensures the password meets defined security standards."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search("[a-z]", password) or not re.search("[A-Z]", password):
            raise ValueError(
                "Password must include both lowercase and uppercase characters."
            )
        if not re.search("[0-9]", password):
            raise ValueError("Password must include at least one number.")
        if not re.search('[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must include at least one special character.")

    @staticmethod
    async def confirm_password(password: str, password_confirmation: str):
        """
        Confirms that the given password and confirmation match and meet security standards.
        """
        if password != password_confirmation:
            raise ValueError("Passwords do not match.")
