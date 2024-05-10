from sqlalchemy.orm import Session
from typing import Optional
from ...models.users.activity.user_activity_model import UserActivity


class UserActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_activity_by_user_id(self, user_id: str) -> Optional[UserActivity]:
        return (
            self.db.query(UserActivity)
            .filter(UserActivity.user_id == user_id)
            .first()
        )

    def update_user_activity(
        self, user_id: str, activity_data: dict
    ) -> Optional[UserActivity]:
        activity = self.get_activity_by_user_id(user_id)
        if activity:
            for key, value in activity_data.items():
                setattr(activity, key, value)
            self.db.commit()
            return activity
        return None

    def list_activities(self, skip: int = 0, limit: int = 10) -> list[UserActivity]:
        """List user activities with pagination."""
        return self.db.query(UserActivity).offset(skip).limit(limit).all()
