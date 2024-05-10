from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import UUID4

from ...database.session import get_db
from ...repositories.user.user_activity_repository import UserActivityRepository
from ...schemas.user.user_activity_schema import UserActivityUpdate, UserActivityRead

router = APIRouter()


@router.get("/{user_id}/activity", response_model=UserActivityRead)
def get_user_activity(user_id: UUID4, request: Request):
    db: Session = request.state.db
    activity_repository = UserActivityRepository(db)
    activity = activity_repository.get_activity_by_user_id(user_id)
    if not activity:
        raise HTTPException(status_code=404, detail="User activity not found")
    return activity


@router.put("/{user_id}/activity", response_model=UserActivityRead)
def update_user_activity(
    user_id: UUID4, activity_data: UserActivityUpdate, request: Request
):
    db: Session = request.state.db
    activity_repository = UserActivityRepository(db)
    updated_activity = activity_repository.update_user_activity(
        user_id, activity_data.dict()
    )
    if not updated_activity:
        raise HTTPException(status_code=404, detail="User activity not found")
    return updated_activity
