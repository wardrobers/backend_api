from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserInfo
from app.repositories.common import (
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)
from app.schemas.users import UserInfoCreate, UserInfoRead, UserInfoUpdate


class UserInfoRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """Repository for managing user information."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.model = UserInfo  # Define the model for this repository

    async def get_user_info_by_user_id(self, user_id: UUID) -> Optional[UserInfoRead]:
        """Gets user info by user ID."""
        async with self.db_session as session:
            user_info = await session.execute(
                select(self.model).where(self.model.user_id == user_id)
            )
            user_info = user_info.scalars().first()
            return UserInfoRead.model_validate(user_info) if user_info else None

    async def create_user_info(
        self, user_id: UUID, user_info_data: UserInfoCreate
    ) -> UserInfoRead:
        """Creates new user info."""
        async with self.db_session as session:
            new_user_info = self.model(**user_info_data.model_dump(), user_id=user_id)
            session.add(new_user_info)
            await session.commit()
            await session.refresh(new_user_info)
            return UserInfoRead.model_validate(new_user_info)

    async def update_user_info(
        self, user_id: UUID, user_info_data: UserInfoUpdate, context: str
    ) -> UserInfoRead:
        """Updates user info."""
        async with self.db_session as session:
            user_info = await self.get_user_info_by_user_id(user_id)
            if not user_info:
                raise HTTPException(status_code=404, detail="User info not found")

            # Apply updates based on context (example):
            if context == "contact_details":
                user_info.phone_number = user_info_data.phone_number
                user_info.email = user_info_data.email
            # ... other context-specific update logic

            await session.commit()
            await session.refresh(user_info)
            return UserInfoRead.model_validate(user_info)

    async def delete_user_info(self, user_id: UUID) -> None:
        """Deletes user info."""
        async with self.db_session as session:
            user_info = await self.get_user_info_by_user_id(user_id)
            if not user_info:
                raise HTTPException(status_code=404, detail="User info not found")

            await session.delete(user_info)
            await session.commit()
