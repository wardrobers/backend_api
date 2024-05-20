import re
from enum import Enum
from sqlalchemy import Column, DateTime, String, Boolean, select, update, insert, delete
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from firebase_admin import auth as firebase_auth

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)

# Import models that are directly related and need explicit import for relationships
from app.models.common import AuthHandler
from app.models.users import UserInfo, UserRoles
from app.models.subscriptions import Subscriptions
from app.models.promotions import UserPromotions


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


class User(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "users"

    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, default=False)
    last_login_at = Column(DateTime)

    # Relationships
    info = relationship("UserInfo", uselist=False, backref="users")
    activity = relationship("UserActivity", uselist=False, backref="users")
    basket = relationship("UserBasket", uselist=False, backref="users")
    photos = relationship("UserPhotos", backref="users")
    role = relationship("Roles", secondary="user_roles", backref="users")
    order = relationship("Order", backref="users")
    subscriptions = relationship("Subscriptions", backref="users")
    reviews_and_ratings = relationship("UserReviewsAndRatings", backref="users")
    saved_items = relationship("UserSavedItems", backref="users")
    promotions = relationship("UserPromotions", backref="users")
    addresses = relationship("UserAddresses", backref="users")
    categories_for_user = relationship("CategoriesForUser", backref="users")
    data_privacy_consents = relationship("DataPrivacyConsents", backref="users")
    transactions = relationship("Transactions", backref="users")

    @classmethod
    async def get_user_by_login(cls, db_session: AsyncSession, login: str):
        """
        Retrieves a user from the database by their login.

        Args:
            login (str): The login of the user to retrieve.

        Returns:
            Optional[User]: The User object if found, otherwise None.
        """
        async with db_session as session:
            result = await session.execute(
                select(cls).where(cls.login == login, cls.deleted_at.is_(None))
            )
            return result.scalars().first()

    async def activate_account(self, db_session: AsyncSession):
        try:
            await db_session.execute(
                update(User).where(User.id == self.id).values(is_active=True)
            )
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

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
            hashed_password = AuthHandler.get_password_hash(user_data["password"])
            user_data["password"] = hashed_password
            user_data["is_active"] = False  # User is inactive until email verification

            # Create the user in the database
            new_user = User(**user_data)
            db_session.add(new_user)
            await db_session.commit()

        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to create user: {str(e)}"
            )

    async def reset_password_basic(self, db_session: AsyncSession, new_password: str):
        hashed_password = AuthHandler.get_password_hash(new_password)
        try:
            await db_session.execute(
                update(User).where(User.id == self.id).values(password=hashed_password)
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
                update(User).where(User.email == email).values(password=hashed_password)
            )
            await db_session.commit()
        except firebase_auth.FirebaseError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail="Invalid or expired reset token."
            )

    async def update_user_info(self, db_session: AsyncSession, updates: dict, context):
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
                update(UserInfo).where(UserInfo.user_id == self.id).values(**updates)
            )
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to update user info: {str(e)}"
            )

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

    async def _add_role(self, db_session: AsyncSession, role_id: int):
        existing_role = await db_session.execute(
            select(UserRoles).where(
                UserRoles.user_id == self.id, UserRoles.role_id == role_id
            )
        )
        if existing_role.scalars().first() is not None:
            raise HTTPException(
                status_code=400, detail="Role already assigned to user."
            )
        await db_session.execute(
            insert(UserRoles).values(user_id=self.id, role_id=role_id)
        )

    async def _remove_role(self, db_session: AsyncSession, role_id: int):
        await db_session.execute(
            delete(UserRoles).where(
                UserRoles.user_id == self.id, UserRoles.role_id == role_id
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
        self, db_session: AsyncSession, subscription_data: dict
    ):
        await db_session.execute(
            update(Subscriptions)
            .where(Subscriptions.user_id == self.id, Subscriptions.is_active == True)
            .values(**subscription_data)
        )

    async def _cancel_subscription(self, db_session: AsyncSession, _):
        await db_session.execute(
            update(Subscriptions)
            .where(Subscriptions.user_id == self.id, Subscriptions.is_active == True)
            .values(is_active=False)
        )

    async def toggle_notifications(
        self, db_session: AsyncSession, enable_notifications: bool
    ):
        """Enables or disables user notifications."""
        try:
            await db_session.execute(
                update(User)
                .where(User.id == self.id)
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
