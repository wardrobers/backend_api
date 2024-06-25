from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config import oauth2_scheme
from app.database import get_db
from app.models.users import Users
from app.schemas.users import (
    UpdateContext,
    UserInfoRead,
    UserInfoUpdate,
    UsersRead,
    UsersUpdate,
)
from app.services.users import AuthService, UserInfoService, UsersService

router = APIRouter()
auth_service = AuthService()
users_service = UsersService()
user_info_service = UserInfoService()


def get_current_active_user(
    db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Users:
    """Dependency to get the currently authenticated user from the JWT token."""
    user = auth_service.get_current_user(db_session, token)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def get_current_user_id(
    current_user: Users = Depends(get_current_active_user),
) -> UUID4:
    """Dependency to get the user_id of the current user."""
    return current_user.id


@router.get("/me", response_model=UsersRead)
def get_current_user_profile(
    current_user: Users = Depends(get_current_active_user),
    db_session: Session = Depends(get_db),
):
    """
    Retrieves the complete profile of the currently authenticated user.

    **Requires Authentication (JWT).**

    **Response (Success - 200 OK):**
        - `UsersRead` (schema): The complete user profile including related info.
    """
    return users_service.get_user_by_id(db_session, current_user.id)


@router.put("/me", response_model=UsersRead)
def update_current_user_profile(
    user_update: UsersUpdate,
    db_session: Session = Depends(get_db),
    current_user: Users = Depends(get_current_active_user),
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
    return users_service.update_user(
        db_session, current_user.id, user_update, current_user
    )


@router.put("/me/info", response_model=UserInfoRead)
def update_current_user_info(
    user_info_update: UserInfoUpdate,
    db_session: Session = Depends(get_db),
    current_user: Users = Depends(get_current_active_user),
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
    return user_info_service.update_user_info(
        db_session, current_user.id, user_info_update, UpdateContext.FULL_PROFILE
    )


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def delete_current_user_account(
    db_session: Session = Depends(get_db),
    current_user: Users = Depends(get_current_active_user),
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
    users_service.delete_user(db_session, current_user.id, current_user)


@router.put("/notifications", status_code=status.HTTP_200_OK, response_model=None)
def update_notification_preferences(
    enabled: bool,
    db_session: Session = Depends(get_db),
    current_user: Users = Depends(get_current_active_user),
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
    users_service.toggle_notifications(
        db_session, current_user.id, enabled, current_user
    )
    return {"message": "Notification preferences updated successfully"}
