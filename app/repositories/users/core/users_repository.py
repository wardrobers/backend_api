from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models.users import Users
from app.repositories.common import BulkActionsMixin, CachingMixin, SearchMixin
from app.schemas.users import UsersUpdate


class UsersRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """
    Repository for core user operations, utilizing mixins for common functionality.
    """

    model = Users
    MAIN_FOREIGN_KEY = "login"

    def get_user_by_login(self, db_session: Session, login: str) -> Users:
        """Retrieves a user by their login."""
        return self.get_by_field(db_session, self.MAIN_FOREIGN_KEY, login)

        # TODO: You can add caching logic here if needed, but ensure
        # that the cache key is generated using the user.id (UUID)
        # if user:
        #     self.invalidate_cache_by_id(user.id, extra_params={"login": login})

    def update_user(
        self, db_session: Session, user: Users, user_data: UsersUpdate
    ) -> Users:
        """Updates a user's information."""

        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        db_session.commit()
        db_session.refresh(user)
        # TODO: Invalidate cache after updating a user
        # self.invalidate_cache_by_id(user.id)
        return user

    def delete_user(self, db_session: Session, user_id: UUID) -> None:
        """Deletes a user."""

        user = self.get_by_id(db_session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        self.delete(db_session)

        # TODO: Invalidate cache after deleting a user
        # self.invalidate_cache_by_id(user_id)

    def toggle_notifications(
        self, db_session: Session, user_id: UUID, enable_notifications: bool
    ) -> None:
        """Toggles user notifications."""

        user = self.get_by_id(db_session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_notificated = enable_notifications
        db_session.commit()

        # TODO: Invalidate cache after toggling notifications
        # self.invalidate_cache_by_id(user.id)

    def activate_account(self, db_session: Session, user_id: UUID) -> None:
        """Activates a user's account."""

        user = self.get_by_id(db_session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = True
        db_session.commit()

        # TODO: Invalidate cache after activating an account
        # self.invalidate_cache_by_id(user.id)

    def reset_password_basic(
        self, db_session: Session, user_id: UUID, new_password: str
    ) -> None:
        """Resets a user's password without token verification."""

        user = self.get_by_id(db_session, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.password = new_password
        db_session.commit()

        # TODO: Invalidate cache after resetting a password
        # self.invalidate_cache_by_id(user.id)
