from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

from .subscription_schema import SubscriptionRead


class SubscriptionTypeBase(BaseModel):
    name: Optional[str] = None
    period_uuid: UUID4
    price: float
    count_free_orders: int


class SubscriptionTypeCreate(SubscriptionTypeBase):
    pass  # All required fields are inherited from SubscriptionTypeBase


class SubscriptionTypeRead(SubscriptionTypeBase):
    uuid: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    subscriptions: list[SubscriptionRead] = []

    class Config:
        orm_mode = True  # Important for ORM compatibility


# For updating an existing SubscriptionType
class SubscriptionTypeUpdate(BaseModel):
    name: Optional[str] = None
    period_uuid: Optional[UUID4] = None
    price: Optional[float] = None
    count_free_orders: Optional[int] = None

    class Config:
        orm_mode = True
