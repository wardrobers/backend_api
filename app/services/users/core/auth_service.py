import datetime
import json
import os
import re
from datetime import timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Users
from app.schemas.users import UserLogin

# Initialize OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Handles user authentication, token management, and password-related operations.

    Features:
    - Secure password hashing using bcrypt.
    - JWT token generation and validation.
    - Password strength validation with customizable rules.
    - Refresh token support (optional).
    - Asynchronous database interactions.
    - Improved error handling.
    - Type hints for enhanced code clarity.
    """

    SECRET_KEY = json.loads(os.environ["AUTH_SECRET_KEY"])["auth_secret_key"]
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

    # Password validation rules
    PASSWORD_REGEX = (
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def authenticate_user(self, login_data: UserLogin) -> Optional[Users]:
        """
        Authenticates a user based on their login and password.
        """
        user = await self.db_session.execute(
            select(Users).filter(Users.login == login_data.login)
        )
        user = user.scalars().first()
        if user and pwd_context.verify(login_data.password, user.password):
            return user
        return None

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Generates a JWT access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now(datetime.UTC) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.UTC) + timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Generates a JWT refresh token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now(datetime.UTC) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.UTC) + timedelta(
                minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> Users:
        """
        Decodes the JWT token, retrieves the user from the database, and raises an exception if
        credentials are invalid or the user is not found.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise self._credentials_exception()
            user = await self.db_session.execute(
                select(Users).filter(Users.login == username)
            )
            user = user.scalars().first()
            if user is None:
                raise self._credentials_exception()
            return user
        except JWTError:
            raise self._credentials_exception()

    async def change_password(self, user: Users, new_password: str) -> None:
        """
        Changes the user's password, handling hashing and database updates.
        """
        self.validate_password_strength(new_password)
        hashed_password = pwd_context.hash(new_password)
        user.password = hashed_password
        await self.db_session.commit()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain password against a hashed password using bcrypt.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def validate_password_strength(self, password: str) -> None:
        """
        Validates password strength against predefined rules. You can customize these rules
        based on your application's security requirements.
        """
        if not re.match(self.PASSWORD_REGEX, password):
            raise ValueError(
                "Password must be at least 8 characters long, contain at least one lowercase letter, "
                "one uppercase letter, one number, and one special character."
            )

    def _credentials_exception(self) -> HTTPException:
        """
        Returns a standardized HTTPException for unauthorized access attempts.
        """
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
