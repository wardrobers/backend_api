from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.users import Users
from app.repositories.users import UserInfoRepository, UsersRepository
from app.schemas.users import (
    UpdateContext,
    UserInfoRead,
    UserInfoUpdate,
    UsersRead,
    UsersUpdate,
)
from app.services.users import AuthService, UsersService

router = APIRouter()


# Dependency to get user service
async def get_user_service(
    db_session: AsyncSession = Depends(get_async_session),
):
    users_repository = UsersRepository(db_session)
    user_info_repository = UserInfoRepository(db_session)
    return UsersService(users_repository, user_info_repository)


@router.get("/me", response_model=UsersRead)
async def get_current_user_profile(
    current_user: Users = Depends(AuthService.get_current_user),
    user_service: UsersService = Depends(get_user_service),
):
    """
    Retrieves the complete profile of the currently authenticated user.

    **Requires Authentication (JWT).**

    **Response (Success - 200 OK):**
        - `UsersRead` (schema): The complete user profile including related info.
    """
    return await user_service.get_user_by_id(current_user.id)


@router.put("/me", response_model=UsersRead)
async def update_current_user_profile(
    user_update: UsersUpdate,
    current_user: Users = Depends(AuthService.get_current_user),
    user_service: UsersService = Depends(get_user_service),
):
    """
    Updates the profile of the currently authenticated user.

    **Requires Authentication (JWT).**

    **Request Body:**
        - `UsersUpdate` (schema): Contains fields to be updated in the 'users' table.

    **Response (Success - 200 OK):**
        - `UsersRead` (schema): The updated user object.

    **Error Codes:**
        - 400 Bad Request: If update data is invalid or a conflict occurs (e.g., duplicate email).
        - 403 Forbidden: If the user is not authorized to update the profile.
    """
    return await user_service.update_user(current_user.id, user_update, current_user)


@router.put("/me/info", response_model=UserInfoRead)
async def update_current_user_info(
    user_info_update: UserInfoUpdate,
    current_user: Users = Depends(AuthService.get_current_user),
    user_service: UsersService = Depends(get_user_service),
):
    """
    Updates additional user info of the currently authenticated user.

    **Requires Authentication (JWT).**

    **Request Body:**
        - `UserInfoUpdate` (schema): Contains fields to be updated in the 'user_info' table.

    **Response (Success - 200 OK):**
        - `UserInfoRead` (schema): The updated user info object.

    **Error Codes:**
        - 400 Bad Request: If update data is invalid.
        - 403 Forbidden: If the user is not authorized to update the info.
        - 404 Not Found: If the user info for the current user is not found.
    """
    return await user_service.update_user_info(
        current_user.id, user_info_update, UpdateContext.FULL_PROFILE
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_current_user_account(
    current_user: Users = Depends(AuthService.get_current_user),
    user_service: UsersService = Depends(get_user_service),
):
    """
    Deletes the account of the currently authenticated user.

    **Requires Authentication (JWT).**

    **Response (Success - 204 No Content):**
        - Indicates successful account deletion.

    **Error Codes:**
        - 403 Forbidden: If the user is not authorized to delete the account.
        - 404 Not Found: If the user is not found.
    """
    await user_service.delete_user(current_user.id, current_user)


@router.put("/notifications", status_code=status.HTTP_200_OK, response_model=None)
async def update_notification_preferences(
    enabled: bool,
    current_user: Users = Depends(AuthService.get_current_user),
    user_service: UsersService = Depends(get_user_service),
):
    """
    Enables or disables notifications for the currently authenticated user.

    **Requires Authentication (JWT).**

    **Request Body:**
        - enabled (bool): `True` to enable notifications, `False` to disable.

    **Response (Success - 200 OK):**
        - `message` (str): A confirmation message.

    **Error Codes:**
        - 403 Forbidden: If the user is not authorized to modify notifications.
        - 404 Not Found: If the user is not found.
    """
    await user_service.toggle_notifications(current_user.id, enabled, current_user)
    return {"message": "Notification preferences updated successfully"}
