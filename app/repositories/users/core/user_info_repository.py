from typing import Optional

from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models.users import UserInfo
from app.repositories.common import BulkActionsMixin, CachingMixin, SearchMixin
from app.schemas.users import UserInfoUpdate


class UserInfoRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """Repository for managing user information."""

    model = UserInfo
    MAIN_FOREIGN_KEY = "user_id"

    def get_user_info_by_user_id(
        self, db_session: Session, user_id: UUID
    ) -> Optional[UserInfo]:
        """Gets user info by user ID."""
        return self.get_by_field(db_session, self.MAIN_FOREIGN_KEY, user_id)

    def create_user_info(
        self, db_session: Session, user_id: UUID, **kwargs
    ) -> UserInfo:
        """Creates new user info."""
        new_instance = self.model(user_id=user_id, **kwargs)
        db_session.add(new_instance)
        db_session.commit()
        db_session.refresh(new_instance)
        return new_instance

    def update_user_info(
        self,
        db_session: Session,
        user_id: UUID,
        user_info_update: UserInfoUpdate,
    ) -> UserInfo:
        """Updates user info."""
        user_info = self.get_user_info_by_user_id(db_session, user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")

        update_data = user_info_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user_info, key, value)

        db_session.commit()
        db_session.refresh(user_info)
        return user_info

    def delete_user_info(self, db_session: Session, user_id: UUID) -> None:
        """Deletes user info."""
        user_info = self.get_user_info_by_user_id(db_session, user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")

        db_session.delete(user_info)
        db_session.commit()
