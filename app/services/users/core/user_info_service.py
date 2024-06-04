# app/services/users/user_service.py
from fastapi import HTTPException
from sqlalchemy.orm import UUID

from app.models.users import UserInfo
from app.repositories.users import UserInfoRepository
from app.schemas.users import UpdateContext, UserInfoCreate, UserInfoUpdate


class UserInfoService:
    """
    Service layer for core user management operations.
    """

    def __init__(
        self,
        user_info_repository: UserInfoRepository,
    ):
        self.user_info_repository = user_info_repository

    # --- User Info Operations ---
    async def get_user_info(self, user_id: UUID) -> UserInfo:
        """Retrieves user info for a given user."""
        user_info = await self.user_info_repository.get_user_info_by_user_id(user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")
        return user_info

    async def create_user_info(
        self, user_id: UUID, user_info_data: UserInfoCreate
    ) -> UserInfo:
        """Creates new user info."""
        return await self.user_info_repository.create_user_info(user_id, user_info_data)

    async def update_user_info(
        self, user_id: UUID, user_info_update: UserInfoUpdate, context: UpdateContext
    ) -> UserInfoUpdate:
        """
        Updates user info based on the provided context.
        """
        user_info = await self.user_info_repository.get_user_info_by_user_id(user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")

        if context == UpdateContext.CONTACT_DETAILS:
            allowed_fields = {"phone_number", "email"}
        elif context == UpdateContext.FULL_PROFILE:
            allowed_fields = {
                "first_name",
                "last_name",
                "phone_number",
                "email",
            }
        elif context == UpdateContext.LENDER_STATUS:
            allowed_fields = {"lender"}
        elif context == UpdateContext.NAME:
            allowed_fields = {
                "first_name",
                "last_name",
            }
        else:
            raise ValueError("Invalid update context")

        update_data = user_info_update.model_dump(exclude_unset=True)
        for field in update_data.keys():
            if field not in allowed_fields:
                raise HTTPException(
                    status_code=400,
                    detail=f"Field '{field}' cannot be updated in this context.",
                )

        updated_user_info = await self.user_info_repository.update_user_info(
            user_id, UserInfoUpdate(**update_data)
        )
        return UserInfoUpdate.model_validate(updated_user_info)

    async def delete_user_info(self, user_id: UUID) -> None:
        """Deletes user info."""
        await self.user_info_repository.delete_user_info(user_id)
