from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import UUID4

from ...database.session import get_db
from ...repositories.user.user_repository import UserRepository
from ...schemas.user.user_schema import UserCreate, UserRead, UserUpdate
from ...schemas.user.user_info_schema import UserInfoUpdate

router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, request: Request):
    db: Session = request.state.db
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_login(user.login)
    if db_user:
        # If a user is found, raise an HTTPException indicating the user already exists
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        # If no user is found, proceed to create a new user
        return user_repository.create_user(user)


@router.get("/get", response_model=UserRead)
def read_user(user_id: UUID4, request: Request):
    db: Session = request.state.db
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/put", response_model=UserRead)
def update_user(user_id: UUID4, user_update: UserUpdate, request: Request):
    db: Session = request.state.db
    user_repository = UserRepository(db)
    updated_user = user_repository.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID4, request: Request):
    db: Session = request.state.db
    user_repository = UserRepository(db)
    if not user_repository.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


@router.get("/get/profile", response_model=UserRead)
def get_user_profile(user_id: UUID4, request: Request):
    """
    Retrieve a single user profile by UUID.
    """
    db: Session = request.state.db
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/patch/profile", response_model=UserRead)
def update_user_profile(
    user_id: UUID4, user_update: UserInfoUpdate, request: Request
):
    """
    Update user profile information.
    """
    db: Session = request.state.db
    user_repository = UserRepository(db)
    updated_user = user_repository.update_user_info(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
