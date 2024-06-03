from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.users import UserInfo, Users
from app.repositories.users import UsersRepository
from app.schemas.users import UserInfoUpdate, UsersUpdate
from app.services.users import AuthService, UpdateContext, UsersService

router = APIRouter()


@router.get("/me")
async def get_current_user_profile(
    current_user: Users = Depends(AuthService.get_current_user),
    db_session: AsyncSession = Depends(get_async_session),
):
    """
    Retrieves the complete profile of the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 200 OK):
        - Users object (including related info, photos, roles, etc.).
    """
    user_repository = UsersRepository(db_session)
    return await user_repository.get_user_by_login(current_user.login)


@router.put("/me")
async def update_current_user_profile(
    user_update: UsersUpdate,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Updates the profile of the currently authenticated user.

    Requires Authentication (JWT).

    Request Body:
        - user_info_update (UserInfoUpdate): Contains fields to be updated in the 'user_info' table.

    Response (Success - 200 OK):
        - Users object (with updated profile information).

    Error Codes:
        - 400 Bad Request: If update data is invalid or a conflict occurs (e.g., duplicate email).
    """
    user_repository = UsersRepository(db_session)
    updated_user = await user_repository.update_user(
        current_user.id, user_update.model_dump(exclude_unset=True)
    )
    return updated_user


@router.put("/me/info", response_model=UserInfo)  # Updated response model
async def update_current_user_info(
    user_info_update: UserInfoUpdate,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Updates additional user info of the currently authenticated user.
    """
    user_repository = UsersRepository(db_session)
    user_service = UsersService(user_repository)
    await user_service.update_user_info(
        current_user.id,
        user_info_update.dict(exclude_unset=True),
        UpdateContext.FULL_PROFILE,
    )
    await db_session.refresh(current_user)
    return current_user.info  # Return updated UserInfo


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user_account(
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Soft deletes the account of the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful account deactivation.
    """
    user_repository = UsersRepository(db_session)
    await user_repository.delete_user(current_user.id)


@router.put("/notifications", status_code=status.HTTP_200_OK)
async def update_notification_preferences(
    enabled: bool,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Enables or disables notifications for the currently authenticated user.

    Requires Authentication (JWT).

    Request Body:
        - enabled (bool): True to enable notifications, False to disable.

    Response (Success - 200 OK):
        - message (str): A confirmation message.
    """
    user_repository = UsersRepository(db_session)
    await user_repository.toggle_notifications(db_session, current_user.id, enabled)
    return {"message": "Notification preferences updated successfully"}
