from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.users import Users
from app.repositories.common import BulkActionsMixin, CachingMixin, SearchMixin
from app.schemas.users import UsersCreate, UsersUpdate


class UsersRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """
    Repository for core user operations, utilizing mixins for common functionality.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.model = Users

    def get_user_by_login(self, login: str) -> Users:
        """Retrieves a user by their login, incorporating caching."""

        # Construct a select statement to query Users by login
        statement = select(self.model).where(
            self.model.login == login, self.model.deleted_at.is_(None)
        )

        # Execute the statement and retrieve the first result
        result = self.db_session.execute(statement)
        user = result.scalars().first()

        # TODO: You can add caching logic here if needed, but ensure
        # that the cache key is generated using the user.id (UUID)
        # if user:
        #     self.invalidate_cache_by_id(user.id, extra_params={"login": login})

        return user

    def create_user(self, user_data: UsersCreate) -> Users:
        """Creates a new user entry in the database."""

        try:
            new_user = self.model(
                **user_data.model_dump(exclude={"password_confirmation"})
            )
            self.db_session.add(new_user)
            self.db_session.commit()
            self.db_session.refresh(new_user)

            # Invalidate cache after creating a new user
            self.invalidate_all_cache()
            return new_user
        except IntegrityError as e:
            self.db_session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Failed to create user: {str(e)}"
            )

    def update_user(self, user: Users, user_data: UsersUpdate) -> Users:
        """Updates a user's information."""

        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self.db_session.commit()
        self.db_session.refresh(user)
        # TODO: Invalidate cache after updating a user
        # self.invalidate_cache_by_id(user.id)
        return user

    def delete_user(self, user_id: UUID) -> None:
        """Deletes a user."""

        user = self.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.delete(session)

        # TODO: Invalidate cache after deleting a user
        # self.invalidate_cache_by_id(user_id)

    def toggle_notifications(self, user_id: UUID, enable_notifications: bool) -> None:
        """Toggles user notifications."""

        user = self.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_notificated = enable_notifications
        self.db_session.commit()

        # TODO: Invalidate cache after toggling notifications
        # self.invalidate_cache_by_id(user.id)

    def activate_account(self, user_id: UUID) -> None:
        """Activates a user's account."""

        user = self.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = True
        self.db_session.commit()

        # TODO: Invalidate cache after activating an account
        # self.invalidate_cache_by_id(user.id)

    def reset_password_basic(self, user_id: UUID, new_password: str) -> None:
        """Resets a user's password without token verification."""

        user = self.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.password = new_password
        self.db_session.commit()

        # TODO: Invalidate cache after resetting a password
        # self.invalidate_cache_by_id(user.id)
