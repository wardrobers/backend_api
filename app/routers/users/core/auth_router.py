from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models.users import Users
from app.repositories.users import UsersRepository
from app.schemas.users import (
    PasswordChange,
    PasswordResetConfirm,
    PasswordResetRequest,
    UserLogin,
    UsersCreate,
    UsersRead,
)
from app.services.users import AuthService, UsersService

router = APIRouter()


# --- Registration ---
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UsersRead)
async def register_user(
    user_create: UsersCreate, db_session: AsyncSession = Depends(get_async_session)
):
    """
    Registers a new user.

    Request Body:
        - login (str): Unique user login.
        - password (str): User's password (at least 8 characters).
        - password_confirmation (str): Confirmation of the password.

    Response (Success - 201 Created):
        - UsersRead: The newly created user object.

    Error Codes:
        - 400 Bad Request:
            - If the login is already in use.
            - If the passwords don't match.
            - If the password doesn't meet strength requirements.
    """
    user_repository = UsersRepository(db_session)
    user_service = UsersService(user_repository)

    return await user_service.register_user(user_create)


# --- Login ---
@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    login_data: UserLogin, db_session: AsyncSession = Depends(get_async_session)
):
    """
    Logs in a user and generates a JWT access token.

    Request Body:
        - login (str): User's login.
        - password (str): User's password.

    Response (Success - 200 OK):
        - access_token (str): JWT access token.
        - token_type (str): Token type (bearer).

    Error Codes:
        - 401 Unauthorized: If the provided credentials are incorrect.
    """
    user_service = UsersService(UsersRepository(db_session))
    user = await user_service.authenticate_user(
        db_session, login_data.login, login_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
        )

    access_token = AuthService.create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}


# --- Password Reset Request ---
@router.post("/password/forgot", status_code=status.HTTP_200_OK)
async def initiate_password_reset(
    reset_request: PasswordResetRequest,  # Use a Pydantic schema
    db_session: AsyncSession = Depends(get_async_session),
):
    """
    Initiates the password reset process.
    In a real application, you'd integrate with an email service to send a reset link.

    Request Body:
        - email (EmailStr): The user's registered email address.

    Response (Success - 200 OK):
        - message (str): A confirmation message.

    Error Codes:
        - 404 Not Found: If no user is found with the provided email.
    """
    user_repository = UsersRepository(db_session)
    user = await user_repository.get_user_by_login(reset_request.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # TODO: Generate a password reset token and send an email to the user
    # Replace the following with your token generation and email sending logic:
    # reset_token = generate_password_reset_token(user)
    # send_password_reset_email(user, reset_token)

    return {"message": "Password reset instructions sent to your email"}


# --- Password Reset Confirmation ---
@router.post("/password/reset", status_code=status.HTTP_200_OK)
async def reset_password(
    reset_data: PasswordResetConfirm, db: AsyncSession = Depends(get_async_session)
):
    """
    Resets a user's password.

    Request Body:
        - token (str): The password reset token.
        - new_password (str): The new password (at least 8 characters).

    Response (Success - 200 OK):
        - message (str): A confirmation message.

    Error Codes:
        - 400 Bad Request:
            - If the token is invalid or expired.
            - If the password doesn't meet strength requirements.
    """
    # TODO: Verify the token, likely from the database or a secure store.
    # If the token is valid, retrieve the corresponding user.

    # Replace the following with your token verification logic:
    # user = verify_password_reset_token(reset_data.token, db)
    # if not user:
    #     raise HTTPException(status_code=400, detail="Invalid or expired token")

    user_service = UsersService(UsersRepository(db))
    try:
        user_service.validate_password_strength(reset_data.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Update the user's password
    hashed_password = AuthService.get_password_hash(reset_data.new_password)
    user.password = hashed_password
    await db.commit()

    return {"message": "Password reset successfully"}


# --- Password Change Route ---
@router.put("/password/change", status_code=status.HTTP_200_OK)
async def change_password(
    password_change: PasswordChange,  # Pydantic schema for password change
    db: AsyncSession = Depends(get_async_session),
    current_user: Users = Depends(AuthService.get_current_user),
):
    """
    Allows authenticated users to change their password.

    Request Body:
        - current_password (str): The user's current password.
        - new_password (str): The desired new password (at least 8 characters).

    Response (Success - 200 OK):
        - message (str): A confirmation message.

    Error Codes:
        - 400 Bad Request:
            - If the current password is incorrect.
            - If the new password doesn't meet strength requirements.
        - 401 Unauthorized: If the user is not authenticated.
    """
    user_repository = UsersRepository(db)
    user_service = UsersService(user_repository)

    # Verify the current password
    if not AuthService.verify_password(
        password_change.current_password, current_user.password
    ):
        raise HTTPException(status_code=400, detail="Incorrect current password")

    # Validate the new password
    try:
        user_service.validate_password_strength(password_change.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Update the password
    hashed_password = AuthService.get_password_hash(password_change.new_password)
    current_user.password = hashed_password
    await db.commit()

    return {"message": "Password changed successfully"}
