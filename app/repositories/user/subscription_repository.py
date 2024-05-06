from typing import List, Optional
from sqlalchemy.orm import Session
from ...models.subscriptions.subscriptions_model import Subscription
from ...schemas.user.subscription_schema import SubscriptionCreate, SubscriptionUpdate


class SubscriptionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_subscription(
        self, subscription_data: SubscriptionCreate
    ) -> Subscription:
        new_subscription = Subscription(**subscription_data.dict())
        self.db.add(new_subscription)
        self.db.commit()
        self.db.refresh(new_subscription)
        return new_subscription

    def get_subscription_by_uuid(self, uuid: str) -> Optional[Subscription]:
        return self.db.query(Subscription).filter(Subscription.uuid == uuid).first()

    def list_subscriptions(self, skip: int = 0, limit: int = 100) -> List[Subscription]:
        return self.db.query(Subscription).offset(skip).limit(limit).all()

    def update_subscription(
        self, uuid: str, subscription_data: SubscriptionUpdate
    ) -> Optional[Subscription]:
        subscription = self.get_subscription_by_uuid(uuid)
        if subscription:
            for key, value in subscription_data.dict(exclude_unset=True).items():
                setattr(subscription, key, value)
            self.db.commit()
            return subscription
        return None

    def delete_subscription(self, uuid: str):
        subscription = self.get_subscription_by_uuid(uuid)
        if subscription:
            self.db.delete(subscription)
            self.db.commit()
