from typing import List, Optional
from sqlalchemy.orm import Session
from ...models.user.subscription_period_model import SubscriptionPeriod
from ...schemas.user.subscription_period_schema import (
    SubscriptionPeriodCreate,
    SubscriptionPeriodUpdate,
)


class SubscriptionPeriodRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_subscription_period(
        self, subscription_period_data: SubscriptionPeriodCreate
    ) -> SubscriptionPeriod:
        new_period = SubscriptionPeriod(**subscription_period_data.dict())
        self.db.add(new_period)
        self.db.commit()
        self.db.refresh(new_period)
        return new_period

    def get_subscription_period_by_uuid(
        self, uuid: str
    ) -> Optional[SubscriptionPeriod]:
        return (
            self.db.query(SubscriptionPeriod)
            .filter(SubscriptionPeriod.uuid == uuid)
            .first()
        )

    def list_subscription_periods(
        self, skip: int = 0, limit: int = 100
    ) -> List[SubscriptionPeriod]:
        return self.db.query(SubscriptionPeriod).offset(skip).limit(limit).all()

    def update_subscription_period(
        self, uuid: str, subscription_period_data: SubscriptionPeriodUpdate
    ) -> Optional[SubscriptionPeriod]:
        period = self.get_subscription_period_by_uuid(uuid)
        if period:
            for key, value in subscription_period_data.dict(exclude_unset=True).items():
                setattr(period, key, value)
            self.db.commit()
            return period
        return None

    def delete_subscription_period(self, uuid: str):
        period = self.get_subscription_period_by_uuid(uuid)
        if period:
            self.db.delete(period)
            self.db.commit()
