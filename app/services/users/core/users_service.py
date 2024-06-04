# app/services/users/user_service.py
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import UUID

from app.models.users import Users
from app.repositories.users import UsersRepository
from app.schemas.users import UsersCreate, UsersUpdate, UserInfoUpdate, UsersRead


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

    async def create_user(self, user_data: UsersCreate, background_tasks: BackgroundTasks) -> Users:
        """
        Registers a new user, handling password validation, uniqueness, 
        and optional welcome email sending. 
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

        new_user = await self.users_repository.create_user(user_data)

        # Send a welcome email in the background (optional):
        background_tasks.add_task(self.send_welcome_email, new_user)

        return new_user

    async def update_user(
        self, user_id: UUID, user_data: UsersUpdate, current_user: Users
    ) -> Users:
        """
        Updates a user's core information, potentially handling authorization.
        """
        # Example authorization check: 
        # if current_user.id != user_id and not current_user.is_admin:
        #     raise HTTPException(status_code=403, detail="Not authorized to update this user")

        return await self.users_repository.update_user(user_id, user_data)

    async def delete_user(self, user_id: UUID, current_user: Users) -> None:
        """
        Deletes a user and associated data, with authorization checks.
        """
        # Authorization (example):
        # if current_user.id != user_id and not current_user.is_admin:
        #     raise HTTPException(status_code=403, detail="Not authorized to delete this user")

        # Cascading Delete Logic (example):
        user_addresses = await self.user_address_repository.get_addresses_by_user_id(user_id)
        for address in user_addresses:
            await self.user_address_repository.delete_user_address(address.id)

        user_photos = await self.user_photo_repository.get_user_photos(user_id)
        for photo in user_photos:
            await self.user_photo_repository.delete_user_photo(user_id, photo.id)

        # Deactivate any active subscriptions
        # ...

        await self.users_repository.delete_user(user_id)

    async def update_user_profile(
        self, user_id: UUID, user_update: UsersUpdate, user_info_update: Optional[UserInfoUpdate] = None
    ) -> Users:
        """
        Updates a user's profile, including both core user data and user info.
        """
        updated_user = await self.users_repository.update_user(user_id, user_update)

        if user_info_update:
            await self.user_info_repository.update_user_info(
                user_id, user_info_update
            )
        return updated_user

    async def get_user_profile(self, user_id: UUID) -> UsersRead:
        """
        Retrieves a complete user profile, including related data.
        """
        user = await self.users_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_info = await self.user_info_repository.get_user_info_by_user_id(user_id)
        user_addresses = await self.user_address_repository.get_addresses_by_user_id(
            user_id
        )
        user_roles = await self.user_role_repository.get_user_roles(user_id)
        user_photos = await self.user_photo_repository.get_user_photos(user_id)
        # ... (Fetch other related data: subscriptions, orders, etc.)

        return UsersRead(
            **user.model_dump(),
            info=user_info,
            addresses=user_addresses,
            roles=user_roles,
            photos=user_photos,
            # ... other related data
        )

    async def send_welcome_email(self, user: Users):
        """
        Sends a welcome email to the newly registered user. 
        """
        # Implement email sending logic here using an email service
        # (e.g., SendGrid, Mailgun).
        # ...
        print(f"Welcome email sent to {user.email}!")

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
