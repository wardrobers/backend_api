from enum import Enum

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserInfo
from app.repositories.users import UsersRepository
from app.schemas.users import UserInfoCreate
from app.services.users import AuthService


class UpdateContext(Enum):
    CONTACT_DETAILS = "contact_details"
    FULL_PROFILE = "full_profile"
    LENDER_STATUS = "lender_status"


class UserInfoService:
    """
    Service layer for managing user information operations.
    """

    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository
        self.auth_handler = AuthService()

    async def create_user_info(self, user_info_data: UserInfoCreate) -> UserInfo:
        """Creates user info."""
        return await self.users_repository.create_user_info(user_info_data)

    async def update_user_info(
        self, db_session: AsyncSession, user_id: UUID, updates: dict, context
    ):
        """Updates user information based on the given context."""
        # Optional: Add context-specific validation or transformation
        if context == UpdateContext.CONTACT_DETAILS:
            allowed_keys = {"phone_number", "email"}
            updates = {key: updates[key] for key in updates if key in allowed_keys}
        elif context == UpdateContext.LENDER_STATUS:
            allowed_keys = {"lender"}
            updates = {key: updates[key] for key in updates if key in allowed_keys}

        try:
            await db_session.execute(
                update(UserInfo).where(UserInfo.user_id == user_id).values(**updates)
            )
            await db_session.commit()
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Failed to update user info: {str(e)}"
            )
