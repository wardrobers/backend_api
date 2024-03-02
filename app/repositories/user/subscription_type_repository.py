from typing import List, Optional
from sqlalchemy.orm import Session
from .models import SubscriptionType
from .schemas import SubscriptionTypeCreate, SubscriptionTypeUpdate

class SubscriptionTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_subscription_type(self, subscription_type_data: SubscriptionTypeCreate) -> SubscriptionType:
        new_subscription_type = SubscriptionType(**subscription_type_data.dict())
        self.db.add(new_subscription_type)
        self.db.commit()
        self.db.refresh(new_subscription_type)
        return new_subscription_type

    def get_subscription_type_by_uuid(self, uuid: str) -> Optional[SubscriptionType]:
        return self.db.query(SubscriptionType).filter(SubscriptionType.uuid == uuid).first()

    def list_subscription_types(self, skip: int = 0, limit: int = 100) -> List[SubscriptionType]:
        return self.db.query(SubscriptionType).offset(skip).limit(limit).all()

    def update_subscription_type(self, uuid: str, subscription_type_data: SubscriptionTypeUpdate) -> Optional[SubscriptionType]:
        subscription_type = self.get_subscription_type_by_uuid(uuid)
        if subscription_type:
            for key, value in subscription_type_data.dict(exclude_unset=True).items():
                setattr(subscription_type, key, value)
            self.db.commit()
            return subscription_type
        return None

    def delete_subscription_type(self, uuid: str):
        subscription_type = self.get_subscription_type_by_uuid(uuid)
        if subscription_type:
            self.db.delete(subscription_type)
            self.db.commit()
