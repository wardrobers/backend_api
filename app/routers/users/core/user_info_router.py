from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.config import oauth2_scheme
from app.database import get_db
from app.models.users import Users
from app.schemas.users import (
    UpdateContext,
    UserInfoRead,
    UserInfoUpdate,
    UserInfoCreate,
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


# --- User Info Related Routes --- 

@router.get("/me/info", dependencies=[Depends(oauth2_scheme)], response_model=UserInfoRead)
def get_current_user_info(
    db_session: Session = Depends(get_db),
    current_user: Users = Depends(get_current_active_user),
):
    """
    Get user info for the currently authenticated user.
    """
    return user_info_service.get_user_info(db_session, current_user.id)

@router.post("/me/info", dependencies=[Depends(oauth2_scheme)], response_model=UserInfoRead)
def create_current_user_info(
    user_info_data: UserInfoCreate,
    db_session: Session = Depends(get_db),
    current_user: Users = Depends(get_current_active_user),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """
    Create user info for the currently authenticated user.
    """
    return user_info_service.create_user_info(
        db_session, current_user.id, user_info_data, background_tasks
    )

@router.put("/me/info", dependencies=[Depends(oauth2_scheme)], response_model=UserInfoRead)
def update_current_user_info(
    user_info_update: UserInfoUpdate,
    context: UpdateContext,  # Specify the update context
    db_session: Session = Depends(get_db),
    current_user: Users = Depends(get_current_active_user),
):
    """
    Update user info for the currently authenticated user.
    The 'context' query parameter determines which fields can be updated.
    """
    return user_info_service.update_user_info(
        db_session, current_user.id, user_info_update, context, current_user.id
    )

@router.delete("/me/info", dependencies=[Depends(oauth2_scheme)], status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user_info(
    db_session: Session = Depends(get_db),
    current_user: Users = Depends(get_current_active_user),
):
    """
    Delete user info for the currently authenticated user.
    """
    user_info_service.delete_user_info(db_session, current_user.id, current_user.id)
    return {"message": "User info deleted successfully"}