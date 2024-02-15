import os
import json

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from google.cloud import secretmanager_v1

from app.models.database import SessionLocal
from app.models.sql import User

# Environment variables
JWT_SECRET = os.getenv("JWT_SECRET")

# OAuth2PasswordBearer instance for token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency for verifying JWT tokens
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


# Dependency to get the current user from the token
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.login == username).first()
    if user is None:
        raise credentials_exception
    return user