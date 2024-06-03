from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Users


class UsersRepository:
    """
    Repository responsible for all database operations related to the Users model.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_login(self, login: str) -> Optional[Users]:
        """Retrieves a user by their login."""
        result = await self.db_session.execute(
            select(Users).where(Users.login == login, Users.deleted_at.is_(None))
        )
        return result.scalars().first()

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

    async def activate_account(self, db_session: AsyncSession, user_id: UUID):
        try:
            await db_session.execute(
                update(Users).where(Users.id == user_id).values(is_active=True)
            )
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
