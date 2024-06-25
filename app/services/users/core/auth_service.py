import datetime
import os
import re
from datetime import timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import oauth2_scheme, pwd_context
from app.models.users import Users
from app.schemas.users import UserLogin


class AuthService:
    """
    Handles user authentication, token management, and password-related operations.

    Features:
    - Secure password hashing using bcrypt.
    - JWT token generation and validation.
    - Password strength validation with customizable rules.
    - Refresh token support (optional).
    -  database interactions.
    - Improved error handling.
    - Type hints for enhanced code clarity.
    """

    SECRET_KEY = os.environ.get("AUTH_SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    # Password validation rules
    PASSWORD_REGEX = (
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    def authenticate_user(
        self, db_session: Session, login_data: UserLogin
    ) -> Optional[Users]:
        """Authenticates a user based on their login and password."""
        user = db_session.query(Users).filter_by(login=login_data.login).first()
        if not user:
            return None
        if not self.verify_password(login_data.password, user.password):
            return None
        return user

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Generates a JWT access token."""
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

    def get_current_user(
        self, db_session: Session, token: str = Depends(oauth2_scheme)
    ) -> Users:
        """Decodes the JWT token and retrieves the user from the database."""
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise self._credentials_exception()
            user = db_session.query(Users).filter_by(login=username).first()
            if user is None:
                raise self._credentials_exception()
            return user
        except JWTError:
            raise self._credentials_exception()

    def change_password(
        self, db_session: Session, user: Users, new_password: str
    ) -> None:
        """Changes the user's password."""
        self.validate_password_strength(new_password)
        hashed_password = self.get_password_hash(new_password)
        user.password = hashed_password
        db_session.commit()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    def validate_password_strength(self, password: str) -> None:
        """Validates password strength against predefined rules."""
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

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hashes the password using bcrypt."""
        return pwd_context.hash(password)
