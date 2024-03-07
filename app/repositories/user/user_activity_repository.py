from sqlalchemy.orm import Session
from typing import Optional
from ...models.user.user_activity_model import UserActivity


class UserActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_activity_by_user_uuid(self, user_uuid: str) -> Optional[UserActivity]:
        return (
            self.db.query(UserActivity)
            .filter(UserActivity.user_uuid == user_uuid)
            .first()
        )

    def update_user_activity(
        self, user_uuid: str, activity_data: dict
    ) -> Optional[UserActivity]:
        activity = self.get_activity_by_user_uuid(user_uuid)
        if activity:
            for key, value in activity_data.items():
                setattr(activity, key, value)
            self.db.commit()
            return activity
        return None

    def list_activities(self, skip: int = 0, limit: int = 10) -> list[UserActivity]:
        """List user activities with pagination."""
        return self.db.query(UserActivity).offset(skip).limit(limit).all()
