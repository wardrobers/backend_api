from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import UUID4

from ...database.session import get_db
from ...repositories.user.user_repository import UserRepository
from ...schemas.user.user_schema import UserCreate, UserRead, UserUpdate
from ...schemas.user.user_info_schema import UserInfoUpdate

router = APIRouter()


@router.post(
    "/register", response_model=UserCreate, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, request: Request):
    db: Session = request.state.db
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_login(user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return user_repository.create_user(user)


@router.get("/{user_uuid}", response_model=UserRead)
def read_user(user_uuid: UUID4, request: Request):
    db: Session = request.state.db
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_uuid(user_uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_uuid}", response_model=UserRead)
def update_user(user_uuid: UUID4, user_update: UserUpdate, request: Request):
    db: Session = request.state.db
    user_repository = UserRepository(db)
    updated_user = user_repository.update_user(user_uuid, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_uuid: UUID4, request: Request):
    db: Session = request.state.db
    user_repository = UserRepository(db)
    if not user_repository.delete_user(user_uuid):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


@router.get("/{user_uuid}/profile", response_model=UserRead)
def get_user_profile(user_uuid: UUID4, request: Request):
    """
    Retrieve a single user profile by UUID.
    """
    db: Session = request.state.db
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_uuid(user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_uuid}/profile", response_model=UserRead)
def update_user_profile(
    user_uuid: UUID4, user_update: UserInfoUpdate, request: Request
):
    """
    Update user profile information.
    """
    db: Session = request.state.db
    user_repository = UserRepository(db)
    updated_user = user_repository.update_user_info(user_uuid, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
