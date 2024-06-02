from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.users import Users
from app.services import UpdateContext
from app.routers.users import auth_handler

router = APIRouter()


@router.get("/me")
async def get_current_user_profile(
    current_user: Users = Depends(auth_handler.get_current_user),
):
    """
    Retrieves the complete profile of the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 200 OK):
        - Users object (including related info, photos, roles, etc.).
    """
    return current_user


@router.put("/me")
async def update_current_user_profile(
    user_info_update,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(auth_handler.get_current_user),
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
    await current_user.update_user_info(
        db_session,
        user_info_update.dict(exclude_unset=True),
        UpdateContext.FULL_PROFILE,
    )
    await db_session.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user_account(
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(auth_handler.get_current_user),
):
    """
    Soft deletes the account of the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful account deactivation.
    """
    await current_user.soft_delete(db_session)


@router.put("/notifications", status_code=status.HTTP_200_OK)
async def update_notification_preferences(
    enabled: bool,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(auth_handler.get_current_user),
):
    """
    Enables or disables notifications for the currently authenticated user.

    Requires Authentication (JWT).

    Request Body:
        - enabled (bool): True to enable notifications, False to disable.

    Response (Success - 200 OK):
        - message (str): A confirmation message.
    """
    current_user.is_notificated = enabled
    await db_session.commit()
    return {"message": "Notification preferences updated successfully"}
