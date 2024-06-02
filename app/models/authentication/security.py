import datetime
import json
import os
from datetime import timedelta
from typing import Optional

import argon2
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users.core.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthHandler:
    """
    Handles user authentication and token management.
    """

    SECRET_KEY = json.loads(os.environ["AUTH_SECRET_KEY"])["auth_secret_key"]
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    async def authenticate_user(
        self, db_session: AsyncSession, username: str, password: str
    ):
        user = await db_session.execute(select(User).filter(User.username == username))
        user = user.scalars().first()
        if not user or not self.verify_password(password, user.hashed_password):
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
        self, db_session: AsyncSession, token: str = Depends(oauth2_scheme)
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
            user = await db_session.execute(
                select(User).filter(User.username == username)
            )
            user = user.scalars().first()
        except JWTError:
            raise credentials_exception
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(self, current_user):
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    @staticmethod
    def get_password_hash(password: str) -> str:
        return argon2.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            return argon2.verify(plain_password, hashed_password)
        except argon2.exceptions.VerifyMismatchError:
            return False
