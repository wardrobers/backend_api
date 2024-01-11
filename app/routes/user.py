from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user
from ..models.pydantic import UserInformation
from ..models.sqlalchemy import User

router = APIRouter()


@router.get("/profile")
async def get_user_profile(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return current_user


@router.put("/profile")
async def update_user_profile(
    user_info: UserInformation,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Update user information logic
    pass
