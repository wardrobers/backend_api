from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Users
from app.repositories.common import (
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)
from app.schemas.users import UsersCreate, UsersUpdate


class UsersRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """
    Repository for core user operations, utilizing mixins for common functionality.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.model = Users

    async def get_user_by_login(self, login: str) -> Users:
        """Retrieves a user by their login, incorporating caching."""
        async with self.db_session as session:
            # Construct a select statement to query Users by login
            statement = select(self.model).where(
                self.model.login == login, self.model.deleted_at.is_(None)
            )

            # Execute the statement and retrieve the first result
            result = await session.execute(statement)
            user = result.scalars().first()

            # TODO: You can add caching logic here if needed, but ensure
            # that the cache key is generated using the user.id (UUID)
            # if user:
            #     await self.invalidate_cache_by_id(user.id, extra_params={"login": login})

            return await user

    async def create_user(self, user_data: UsersCreate) -> Users:
        """Creates a new user entry in the database."""
        async with self.db_session as session:
            try:
                new_user = self.model(
                    **user_data.model_dump(exclude={"password_confirmation"})
                )
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)

                # Invalidate cache after creating a new user
                await self.invalidate_all_cache()
                return new_user
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(
                    status_code=400, detail=f"Failed to create user: {str(e)}"
                )

    async def update_user(self, user: Users, user_data: UsersUpdate) -> Users:
        """Updates a user's information."""
        async with self.db_session as session:
            for field, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)
            await session.commit()
            await session.refresh(user)
            # TODO: Invalidate cache after updating a user
            # await self.invalidate_cache_by_id(user.id)
            return user

    async def delete_user(self, user_id: UUID) -> None:
        """Deletes a user."""
        async with self.db_session as session:
            user = await self.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            await user.delete(session)

            # TODO: Invalidate cache after deleting a user
            # await self.invalidate_cache_by_id(user_id)

    async def toggle_notifications(
        self, user_id: UUID, enable_notifications: bool
    ) -> None:
        """Toggles user notifications."""
        async with self.db_session as session:
            user = await self.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            user.is_notificated = enable_notifications
            await session.commit()

            # TODO: Invalidate cache after toggling notifications
            # await self.invalidate_cache_by_id(user.id)

    async def activate_account(self, user_id: UUID) -> None:
        """Activates a user's account."""
        async with self.db_session as session:
            user = await self.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user.is_active = True
            await session.commit()

            # TODO: Invalidate cache after activating an account
            # await self.invalidate_cache_by_id(user.id)

    async def reset_password_basic(self, user_id: UUID, new_password: str) -> None:
        """Resets a user's password without token verification."""
        async with self.db_session as session:
            user = await self.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            user.password = new_password
            await session.commit()

            # TODO: Invalidate cache after resetting a password
            # await self.invalidate_cache_by_id(user.id)
