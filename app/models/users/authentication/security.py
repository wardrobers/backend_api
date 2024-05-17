import os
import json
import argon2
import datetime
from datetime import timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.models.users import User



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthHandler:
    SECRET_KEY = json.loads(os.environ["AUTH_SECRET_KEY"])["auth_secret_key"]
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def get_password_hash(self, password: str) -> str:
        return argon2.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return argon2.verify(plain_password, hashed_password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def authenticate_user(
        self, db_session: Session, username: str, password: str
    ):
        user_repo = User(db_session)
        user = user_repo.get_user_by_login(
            username
        )  # Assuming this method exists and returns a user entity
        if not user or not self.verify_password(
            password, user.password
        ):  # Ensure you're using the correct attribute for the password
            return None
        return user

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        else:
            expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def get_current_user(
        self, db_session: Session, token: str = Depends(oauth2_scheme)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            user_repo = User(db_session)
            user = user_repo.get_user_by_login(
                username
            )  # Using UserRepository to fetch user
        except JWTError:
            raise credentials_exception
        if user is None:
            raise credentials_exception
        return user

    # If you have specific logic to determine if a user is active or not,
    # implement it in this method.
    async def get_current_active_user(
        self, current_user
    ):
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
