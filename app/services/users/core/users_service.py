# app/services/users/user_service.py
from fastapi import HTTPException
from sqlalchemy.orm import UUID

from app.models.users import Users
from app.repositories.users import UsersRepository
from app.schemas.users import UsersCreate, UsersUpdate


class UsersService:
    """
    Service layer for core user management operations.
    """

    def __init__(
        self,
        users_repository: UsersRepository,
    ):
        self.users_repository = users_repository

    # --- Core User Operations ---
    async def get_user_by_id(self, user_id: UUID) -> Users:
        user = await self.users_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_user_by_login(self, login: str) -> Users:
        user = await self.users_repository.get_user_by_login(login)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_all_users(self) -> list[Users]:
        return await self.users_repository.get_all_users()

    async def create_user(self, user_data: UsersCreate) -> Users:
        """
        Registers a new user after performing necessary checks.
        """
        if user_data.password != user_data.password_confirmation:
            raise HTTPException(status_code=400, detail="Passwords don't match")

        existing_user = await self.users_repository.get_user_by_login(user_data.login)
        if existing_user:
            raise HTTPException(status_code=400, detail="Login already in use")

        try:
            self.validate_password_strength(user_data.password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return await self.users_repository.create_user(user_data)

    async def update_user(self, user_id: UUID, user_data: UsersUpdate) -> Users:
        """Updates a user."""
        return await self.users_repository.update_user(user_id, user_data)

    async def delete_user(self, user_id: UUID) -> None:
        """Deletes a user."""
        # Delete related data (user info, addresses, etc.) using other service methods
        # ... (Implement deletion logic for related entities)

        await self.users_repository.delete_user(user_id)

    async def activate_account(self, user_id: UUID) -> None:
        """Activates a user's account."""
        await self.users_repository.activate_account(user_id)

    async def reset_password_basic(self, user_id: UUID, new_password: str) -> None:
        """Resets the user's password (used if token verification is not implemented)."""
        await self.users_repository.reset_password_basic(user_id, new_password)

    async def toggle_notifications(
        self, user_id: UUID, enable_notifications: bool
    ) -> None:
        """Toggles user notifications on or off."""
        await self.users_repository.toggle_notifications(user_id, enable_notifications)
