from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

from app.models.users import UserInfo
from app.schemas.users import UserInfoCreate, UserInfoUpdate


class UserInfoRepository:
    """Repository for managing user information."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_info_by_user_id(self, user_id: UUID) -> Optional[UserInfo]:
        """Gets user info by user ID."""
        user_info = await self.db_session.execute(
            select(UserInfo).where(UserInfo.user_id == user_id)
        )
        return user_info.scalars().first()

    async def create_user_info(
        self, user_id: UUID, user_info_data: UserInfoCreate
    ) -> UserInfo:
        """Creates new user info."""
        new_user_info = UserInfo(**user_info_data.model_dump(), user_id=user_id)
        await new_user_info.create(self.db_session)
        return new_user_info

    async def update_user_info(
        self, user_id: UUID, user_info_data: UserInfoUpdate
    ) -> UserInfo:
        """Updates user info."""
        user_info = await self.get_user_info_by_user_id(user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")
        await user_info.update(
            self.db_session, **user_info_data.model_dump(exclude_unset=True)
        )
        return user_info

    async def delete_user_info(self, user_id: UUID) -> None:
        """Deletes user info."""
        user_info = await self.get_user_info_by_user_id(user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")
        await user_info.delete(self.db_session)
