from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import UUID4

from ..models import UserActivity
from ..dependencies import get_db
from ..repositories.user_activity_repository import UserActivityRepository
from ..schemas.user_activity_schema import UserActivityUpdate, UserActivityRead

router = APIRouter()

@router.get("/users/{user_uuid}/activity", response_model=UserActivity)
def get_user_activity(user_uuid: UUID4, db: Session = Depends(get_db)):
    activity_repository = UserActivityRepository(db)
    activity = activity_repository.get_activity_by_user_uuid(user_uuid)
    if not activity:
        raise HTTPException(status_code=404, detail="User activity not found")
    return activity

@router.put("/users/{user_uuid}/activity", response_model=UserActivityRead)
def update_user_activity(user_uuid: UUID4, activity_data: UserActivityUpdate, db: Session = Depends(get_db)):
    activity_repository = UserActivityRepository(db)
    updated_activity = activity_repository.update_user_activity(user_uuid, activity_data.dict())
    if not updated_activity:
        raise HTTPException(status_code=404, detail="User activity not found")
    return updated_activity