# app/schemas/user/user_schema.py
from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel


class SubscriptionAction(Enum):
    ADD = "add"
    UPDATE = "update"
    CANCEL = "cancel"


# Basic User Schemas
class SubscriptionBase(BaseModel):
    subscription_start: datetime
    subscription_finish: datetime
    count_free_orders: int = 0
    count_orders_available_by_subscription: int = 0
    count_orders_closed_by_subscription: int = 0
    purchase_url: str = None


class SubscriptionCreate(SubscriptionBase):
    subscription_type_id: UUID4


class SubscriptionRead(SubscriptionBase):
    id: UUID4
    user_id: UUID4
    subscription_type_id: UUID4


class SubscriptionUpdate(SubscriptionBase):
    # You might not need all fields to be updatable.
    # Choose the ones that make sense.
    pass


class SubscriptionCancel(BaseModel):
    id: UUID4
