from typing import Optional

from fastapi import HTTPException, status
from pydantic import UUID4

from app.models.users import Users
from app.repositories.users import UsersRepository
from app.schemas.users import (
    UserInfoCreate,
    UserInfoRead,
    UserInfoUpdate,
    UserLogin,
    UsersCreate,
    UsersRead,
    UsersUpdate,
)
from app.services.users.core.auth_service import AuthService


class UsersService:
    """
    Service layer for core user management operations, utilizing repositories
    with mixins for enhanced functionality and code reuse.
    """

    def __init__(
        self,
        users_repository: UsersRepository,
    ):
        self.users_repository = users_repository

    async def get_user_by_id(self, user_id: UUID4) -> UsersRead:
        """Retrieves a user by their ID."""
        user = await self.users_repository.get_by_id(
            self.users_repository.db_session, user_id
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UsersRead.model_validate(user)

    async def get_user_by_login(self, login: str) -> UsersRead:
        """Retrieves a user by their login."""
        user = await self.users_repository.get_user_by_login(login)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UsersRead.model_validate(user)

    async def get_all_users(self) -> list[UsersRead]:
        """Retrieves all users."""
        users = await self.users_repository.get_all(self.users_repository.db_session)
        return [UsersRead.model_validate(user) for user in users]

    async def create_user(self, user_data: UsersCreate) -> UsersRead:
        """
        Registers a new user.
        """
        if user_data.password != user_data.password_confirmation:
            raise HTTPException(status_code=400, detail="Passwords don't match")

        existing_user = await self.users_repository.get_user_by_login(user_data.login)
        if existing_user:
            raise HTTPException(status_code=400, detail="Login already in use")

        try:
            AuthService.validate_password_strength(user_data.password)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        user_data.password = AuthService.get_password_hash(user_data.password)
        new_user = await self.users_repository.create_user(user_data)

        # Optional: Create associated user info
        await self.user_info_repository.create_user_info(
            new_user.id,
            UserInfoCreate(email=new_user.login, first_name="", last_name=""),
        )

        return UsersRead.model_validate(new_user)

    async def update_user(
        self, user_id: UUID4, user_data: UsersUpdate, current_user: Users
    ) -> Users:
        """
        Updates a user's core information.
        """
        # Authorization check:
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this user",
            )

        return await self.users_repository.update_user(user_id, user_data)

    async def authenticate_user(self, login_data: UserLogin) -> Optional[Users]:
        """Authenticates a user based on login and password."""
        user = await self.users_repository.get_user_by_login(login_data.login)
        if not user or not AuthService.verify_password(
            login_data.password, user.password
        ):
            return None
        return user

    async def delete_user(self, user_id: UUID4, current_user: Users) -> None:
        """
        Deletes a user and associated data.
        """
        # Authorization check:
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this user",
            )

        async with self.users_repository.db_session as session:
            # Cascading Delete Logic
            user_addresses = (
                await self.user_address_repository.get_addresses_by_user_id(user_id)
            )
            for address in user_addresses:
                await self.user_address_repository.delete_user_address(address.id)

            user_photos = await self.user_photo_repository.get_user_photos(user_id)
            for photo in user_photos:
                await self.user_photo_repository.delete_user_photo(user_id, photo.id)

            await self.users_repository.delete_user(user_id)

    async def update_user_info(
        self, user_id: UUID4, user_info_update: UserInfoUpdate, context: str
    ) -> UserInfoRead:
        """
        Updates additional user info.
        """
        updated_user_info = await self.user_info_repository.update_user_info(
            user_id, user_info_update, context
        )
        return UserInfoRead.model_validate(updated_user_info)

    async def toggle_notifications(
        self, user_id: UUID4, enable_notifications: bool, current_user: Users
    ) -> None:
        """Toggles user notifications on or off."""
        # Authorization check:
        if current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this user's notifications",
            )

        await self.users_repository.toggle_notifications(user_id, enable_notifications)
