from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models.users import UserInfo
from app.repositories.common import BulkActionsMixin, CachingMixin, SearchMixin
from app.schemas.users import UserInfoCreate, UserInfoRead, UserInfoUpdate


class UserInfoRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """Repository for managing user information."""

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.model = UserInfo  # Define the model for this repository

    def get_user_info_by_user_id(self, user_id: UUID) -> Optional[UserInfoRead]:
        """Gets user info by user ID."""

        user_info = self.db_session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        user_info = user_info.scalars().first()
        return UserInfoRead.model_validate(user_info) if user_info else None

    def create_user_info(
        self, user_id: UUID, user_info_data: UserInfoCreate
    ) -> UserInfoRead:
        """Creates new user info."""

        new_user_info = self.model(**user_info_data.model_dump(), user_id=user_id)
        self.db_session.add(new_user_info)
        self.db_session.commit()
        self.db_session.refresh(new_user_info)
        return UserInfoRead.model_validate(new_user_info)

    def update_user_info(
        self, user_id: UUID, user_info_data: UserInfoUpdate, context: str
    ) -> UserInfoRead:
        """Updates user info."""

        user_info = self.get_user_info_by_user_id(user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")

        # Apply updates based on context (example):
        if context == "contact_details":
            user_info.phone_number = user_info_data.phone_number
            user_info.email = user_info_data.email
        # ... other context-specific update logic

        self.db_session.commit()
        self.db_session.refresh(user_info)
        return UserInfoRead.model_validate(user_info)

    def delete_user_info(self, user_id: UUID) -> None:
        """Deletes user info."""

        user_info = self.get_user_info_by_user_id(user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")

        self.db_session.delete(user_info)
        self.db_session.commit()
