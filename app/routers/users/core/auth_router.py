from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.authentication import AuthHandler
from app.models.users import User
from app.database import get_async_session
from app.routers.users import auth_handler


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_create, 
    db_session: AsyncSession = Depends(get_async_session)
):
    """
    Registers a new user.

    Request Body:
        - login (str): Unique user login.
        - password (str): User's password.
        - password_confirmation (str): Confirmation of the user's password. 

    Response (Success - 201 Created):
        - UserRead (schema)

    Error Codes:
        - 400 Bad Request: If the login is already in use or passwords don't match. 
    """
    if user_create.password != user_create.password_confirmation:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    existing_user = await User.get_user_by_login(db_session, user_create.login)
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already in use")

    try: 
        User.validate_password_strength(user_create.password) 
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    hashed_password = AuthHandler.get_password_hash(user_create.password)
    new_user = User(login=user_create.login, password=hashed_password)
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(login_data, db_session: AsyncSession = Depends(get_async_session)):
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
    user = await auth_handler.authenticate_user(
        db_session, login_data.login, login_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect login or password")

    access_token = auth_handler.create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/password/forgot", status_code=status.HTTP_200_OK)
async def initiate_password_reset(
    email, db_session: AsyncSession = Depends(get_async_session)
):
    """
    Initiates the password reset process.
    For simplicity, we'll assume the token is generated and sent via email here.
    In a real application, you'd integrate with an email service.

    Request Body:
        - email (EmailStr): The user's registered email address.

    Response (Success - 200 OK):
        - message (str): A confirmation message.

    Error Codes:
        - 404 Not Found: If no user is found with the provided email address.
    """
    user = await User.get_user_by_login(db_session, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # TODO: Generate and send a password reset token to the user's email
    # Replace this with your actual token generation and email sending logic
    print(f"Password reset token for {email}: {generate_password_reset_token(email)}")
    return {"message": "Password reset instructions sent to your email"}


@router.post("/password/reset", status_code=status.HTTP_200_OK)
async def reset_password(
    reset_data, 
    db: AsyncSession = Depends(get_async_session),
):
    """
    Resets a user's password using a reset token (for future email verification)
    or directly with the old password. 

    Request Body:
        - token (str, optional): Password reset token.
        - old_password (str, optional): User's current password.
        - new_password (str): User's new password.

    Response (Success - 200 OK):
        - message (str): A confirmation message.

    Error Codes:
        - 400 Bad Request: If token is invalid, old password is incorrect,
                          or no reset method is provided.
        - 404 Not Found: If no user is found with the token or login.
    """
    user = None
    if reset_data.token:
        # Future email-based reset logic
        user = verify_password_reset_token(reset_data.token, db)  
        if not user:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
    elif reset_data.old_password:
        # Basic reset with old password
        user = await User.get_user_by_login(db, reset_data.login)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not auth_handler.verify_password(reset_data.old_password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect old password")
    else:
        raise HTTPException(status_code=400, detail="No password reset method provided")

    hashed_password = AuthHandler.get_password_hash(reset_data.new_password)
    user.password = hashed_password
    await db.commit()
    return {"message": "Password reset successfully"}
