from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.authentication import AuthHandler
from app.models.users import User
from app.database import get_async_session


# Initialize the routers and AuthHandler
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users_router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(oauth2_scheme)])
auth_handler = AuthHandler()


@users_router.get("/me")
async def get_current_user_profile(
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Retrieves the complete profile of the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 200 OK):
        - UserRead (schema): A JSON representation of the user's profile data.
    """
    return current_user


@users_router.put("/me")
async def update_current_user_profile(
    user_update,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Updates the profile of the currently authenticated user.

    Requires Authentication (JWT).

    Request Body:
        - UserUpdate (schema): A JSON object containing user fields to be updated
                                (all fields are optional for partial updates).

    Response (Success - 200 OK):
        - UserRead (schema): A JSON representation of the updated user profile.

    Error Codes:
        - 400 Bad Request: If the provided update data is invalid
                          or results in a conflict (e.g., duplicate login).
    """
    if user_update.login:
        existing_user = await User.get_user_by_login(db_session, user_update.login)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Login already in use")

    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "user_info":
            for info_key, info_value in value.items():
                setattr(current_user.info, info_key, info_value)
        else:
            setattr(current_user, key, value)

    await db_session.commit()
    await db_session.refresh(current_user)
    return current_user


@users_router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user_account(
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Soft deletes the account of the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful account deactivation.
    """
    await current_user.soft_delete(db_session)
