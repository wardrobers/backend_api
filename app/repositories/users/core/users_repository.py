from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

from app.models.users import Users
from app.schemas.users import UsersCreate, UsersUpdate


class UsersRepository:
    """
    Repository for core user operations.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_id(self, user_id: UUID) -> Optional[Users]:
        """Retrieves a user by their ID."""
        return await Users.get_by_id(self.db_session, user_id)

    async def get_user_by_login(self, login: str) -> Optional[Users]:
        """Retrieves a user by their login."""
        result = await self.db_session.execute(
            select(Users).where(Users.login == login, Users.deleted_at.is_(None))
        )
        return result.scalars().first()

    async def get_all_users(self) -> list[Users]:
        """Retrieves all users."""
        return await Users.get_all(self.db_session)

    async def create_user(self, user_data: UsersCreate) -> Users:
        """Creates a new user entry in the database."""
        try:
            new_user = Users(**user_data.model_dump(exclude={"password_confirmation"}))
            await new_user.create(self.db_session)
            return new_user
        except IntegrityError as e:
            await self.db_session.rollback()
            raise HTTPException(
                status_code=400, detail=f"Failed to create user: {str(e)}"
            )

    async def update_user(self, user_id: UUID, user_data: UsersUpdate) -> Users:
        """Updates a user's information."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await user.update(self.db_session, **user_data.model_dump(exclude_unset=True))
        return user

    async def delete_user(self, user_id: UUID) -> None:
        """Deletes a user."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await user.delete(self.db_session)

    async def toggle_notifications(
        self, user_id: UUID, enable_notifications: bool
    ) -> None:
        """Toggles user notifications."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_notificated = enable_notifications
        await self.db_session.commit()

    async def activate_account(self, user_id: UUID) -> None:
        """Activates a user's account."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = True
        await self.db_session.commit()

    async def reset_password_basic(self, user_id: UUID, new_password: str) -> None:
        """Resets a user's password without token verification."""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.password = new_password
        await self.db_session.commit()
