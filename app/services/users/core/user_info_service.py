from typing import Optional

from fastapi import HTTPException, BackgroundTasks
from pydantic import UUID4

from app.repositories.users import UserInfoRepository
from app.schemas.users import (
    UpdateContext,
    UserInfoCreate,
    UserInfoRead,
    UserInfoUpdate,
)
# TODO: from app.services.email import send_welcome_email


class UserInfoService:
    """
    Service layer for managing user information, utilizing the UserInfoRepository 
    for database interactions. Includes advanced logic and business-specific methods.
    """

    def __init__(self, user_info_repository: UserInfoRepository):
        self.user_info_repository = user_info_repository

    async def get_user_info(self, user_id: UUID4) -> UserInfoRead:
        """Retrieves user info for a given user."""
        user_info = await self.user_info_repository.get_user_info_by_user_id(user_id)
        if not user_info:
            raise HTTPException(status_code=404, detail="User info not found")
        return UserInfoRead.model_validate(user_info)

    async def create_user_info(
        self, user_id: UUID4, user_info_data: UserInfoCreate, background_tasks: BackgroundTasks
    ) -> UserInfoRead:
        """
        Creates new user info and optionally sends a welcome email.
        """
        user_info = await self.user_info_repository.create_user_info(user_id, user_info_data)

        # TODO: Add a background task to send a welcome email
        # if user_info.email:
        #     background_tasks.add_task(send_welcome_email, user_info.email)

        return UserInfoRead.model_validate(user_info)

    async def update_user_info(
        self,
        user_id: UUID4,
        user_info_update: UserInfoUpdate,
        context: UpdateContext,
        current_user_id: Optional[UUID4] = None,  # Optional: for authorization
    ) -> UserInfoRead:
        """
        Updates user info based on the provided context. 
        Includes basic authorization logic (example).
        """
        if current_user_id and user_id != current_user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to update this user info."
            )

        # Apply updates based on context:
        allowed_fields = self._get_allowed_fields(context)

        update_data = user_info_update.model_dump(exclude_unset=True)
        for field in update_data.keys():
            if field not in allowed_fields:
                raise HTTPException(
                    status_code=400,
                    detail=f"Field '{field}' cannot be updated in this context.",
                )

        updated_info = await self.user_info_repository.update_user_info(
            user_id, UserInfoUpdate(**update_data), context.value
        )
        return UserInfoRead.model_validate(updated_info)

    def _get_allowed_fields(self, context: UpdateContext) -> set[str]:
        """
        Returns a set of allowed fields for update based on the provided context.
        """
        if context == UpdateContext.CONTACT_DETAILS:
            return {"phone_number", "email"}
        elif context == UpdateContext.FULL_PROFILE:
            return {"first_name", "last_name", "phone_number", "email"}
        elif context == UpdateContext.LENDER_STATUS:
            return {"lender"}
        elif context == UpdateContext.NAME:
            return {"first_name", "last_name"}
        else:
            raise ValueError("Invalid update context")

    async def delete_user_info(self, user_id: UUID4, current_user_id: UUID4) -> None:
        """
        Deletes user info. Includes basic authorization logic (example).
        """
        # Authorization Check (Example - assuming only the user can delete their info):
        if user_id != current_user_id:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this user info."
            )
        
        await self.user_info_repository.delete_user_info(user_id)

    # --- Additional Business Logic Methods ---

    async def set_user_as_lender(self, user_id: UUID4) -> UserInfoRead:
        """
        Sets the user's lender status to True.
        You can add any additional logic related to becoming a lender here.
        """
        user_info = await self.get_user_info(user_id)
        if user_info.lender:
            raise HTTPException(status_code=400, detail="User is already a lender.")

        updated_info = await self.user_info_repository.update_user_info(
            user_id, UserInfoUpdate(lender=True), UpdateContext.LENDER_STATUS
        )
        return UserInfoRead.model_validate(updated_info)

    async def verify_email(self, user_id: UUID4, verification_token: str) -> None:
        """
        Verifies the user's email address using a verification token.
        You'll need to implement token generation and storage mechanisms.
        """
        # TODO: Implement email verification logic
        # 1. Retrieve the user's info.
        # 2. Check if the token is valid and matches the user.
        # 3. If valid, update the user's info to mark the email as verified.
        pass

    async def get_public_user_info(self, user_id: UUID4) -> UserInfoRead:
        """
        Returns a subset of user info that is safe to share publicly.
        """
        user_info = await self.get_user_info(user_id)

        # Example: Only return first name and last initial
        return UserInfoRead(
            first_name=user_info.first_name, last_name=user_info.last_name[0] + "."
        )