import os
import json
import argon2
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from ..repositories.user.user_repository import (
    UserRepository,
)  # Update this import based on your project structure
from ..schemas.user.user_schema import UserRead  # Adjust import as necessary
from ..database.session import get_db


SECRET_KEY = json.loads(os.environ["AUTH_SECRET_KEY"])["auth_secret_key"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthHandler:
    def get_password_hash(self, password: str) -> str:
        return argon2.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return argon2.verify(plain_password, hashed_password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    def authenticate_user(
        self, db: Session, username: str, password: str
    ) -> Optional[UserRead]:
        user_repo = UserRepository(db)
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
            expire = datetime.now(datetime.UTC) + expires_delta
        else:
            expire = datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(
        self, db: Session, token: str = Depends(oauth2_scheme)
    ) -> UserRead:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            user_repo = UserRepository(db)
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
        self, current_user: UserRead = Depends(get_current_user)
    ) -> UserRead:
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
