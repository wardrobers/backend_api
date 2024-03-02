from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4

from ..dependencies import get_db
from ..repositories.user_repository import UserRepository
from ..schemas.user_schema import UserCreate, UserRead, UserUpdate
from ..schemas.user_info_schema import UserInfoUpdate

router = APIRouter()

@router.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_login(user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Login already in use")
    return user_repository.create_user(user)

@router.get("/users/{user_uuid}", response_model=UserRead)
def read_user(user_uuid: UUID4, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_uuid(user_uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_uuid}", response_model=UserRead)
def update_user(user_uuid: UUID4, user_update: UserUpdate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    updated_user = user_repository.update_user(user_uuid, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_uuid: UUID4, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    if not user_repository.delete_user(user_uuid):
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

@router.get("/users/{user_uuid}/profile", response_model=UserRead)
def get_user_profile(user_uuid: UUID4, db: Session = Depends(get_db)):
    """
    Retrieve a single user profile by UUID.
    """
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_uuid(user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/users/{user_uuid}/profile", response_model=UserRead)
def update_user_profile(user_uuid: UUID4, user_update: UserInfoUpdate, db: Session = Depends(get_db)):
    """
    Update user profile information.
    """
    user_repository = UserRepository(db)
    updated_user = user_repository.update_user_info(user_uuid, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user