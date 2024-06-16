from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.users import Users
from app.repositories.users import UsersRepository
from app.schemas.users import (
    PasswordChange,
    PasswordResetConfirm,
    UserLogin,
    UsersCreate,
    UsersRead,
)
from app.services.users import AuthService, UsersService

router = APIRouter()


# Dependency to get user service
def get_user_service(
    db_session: Session = Depends(get_db),
):
    auth_service = AuthService(db_session)
    users_repository = UsersRepository(db_session)
    return UsersService(users_repository, auth_service)


# Dependency for AuthService
def get_auth_service(db_session: Session = Depends(get_db)):
    return AuthService(db_session)


# --- Registration ---
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UsersRead)
def register_user(
    user_create: UsersCreate,
    user_service: UsersService = Depends(get_user_service),
):
    """
    Registers a new user.

    **Request Body:**
        - `UsersCreate` (schema): The new user data.

    **Response (Success - 201 Created):**
        - `UsersRead` (schema): The newly created user object.

    **Error Codes:**
        - 400 Bad Request:
            - If the login is already in use.
            - If the passwords don't match.
            - If the password doesn't meet strength requirements.
    """
    return user_service.create_user(user_create)


# --- Login ---
@router.post("/login", status_code=status.HTTP_200_OK, response_model=None)
def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UsersService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Logs in a user using the OAuth2 password flow and generates a JWT access token.

    **Request Body:**
        - `OAuth2PasswordRequestForm` (from FastAPI): Contains 'username' (login) and 'password' fields.

    **Response (Success - 200 OK):**
        - `access_token` (str): JWT access token.
        - `token_type` (str): Token type (bearer).

    **Error Codes:**
        - 401 Unauthorized: If the provided credentials are incorrect.
    """
    user = user_service.authenticate_user(
        UserLogin(login=form_data.username, password=form_data.password)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )

    access_token = auth_service.create_access_token(data={"sub": user.login})
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- Password Reset Confirmation ---
@router.post("/password/reset", status_code=status.HTTP_200_OK, response_model=None)
def reset_password(
    reset_data: PasswordResetConfirm,
):
    """
    Resets a user's password using a token.

    **Request Body:**
        - `PasswordResetConfirm` (schema): Contains 'token' and 'new_password' fields.

    **Response (Success - 200 OK):**
        - `message` (str): A confirmation message.

    **Error Codes:**
        - 400 Bad Request:
            - If the token is invalid or expired.
            - If the new password doesn't meet strength requirements.
        - 404 Not Found: If no user is associated with the token.
    """
    # TODO: Retrieve the user associated with the reset token.
    # user = get_user_by_reset_token(db_session, reset_data.token)

    # if not user:
    #     raise HTTPException(status_code=404, detail="Invalid or expired token")

    try:
        AuthService.validate_password_strength(reset_data.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Update the user's password
    # user.password = AuthService.get_password_hash(reset_data.new_password)
    # db_session.commit()

    return {"message": "Password reset successfully"}


# --- Password Change Route ---
@router.put("/password/change", status_code=status.HTTP_200_OK, response_model=None)
def change_password(
    password_change: PasswordChange,
    current_user: Users = Depends(AuthService.get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Allows authenticated users to change their password.

    **Requires Authentication (JWT).**

    **Request Body:**
        - `PasswordChange` (schema): Contains 'current_password' and 'new_password' fields.

    **Response (Success - 200 OK):**
        - `message` (str): A confirmation message.

    **Error Codes:**
        - 400 Bad Request:
            - If the current password is incorrect.
            - If the new password doesn't meet strength requirements.
        - 401 Unauthorized: If the user is not authenticated.
    """
    # Verify the current password
    if not auth_service.verify_password(
        password_change.current_password, current_user.password
    ):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    # Validate the new password
    try:
        auth_service.validate_password_strength(password_change.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Update the password
    auth_service.change_password(current_user, password_change.new_password)

    return {"message": "Password changed successfully"}
