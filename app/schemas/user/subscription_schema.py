from pydantic import BaseModel, UUID4, Field
from typing import Optional, List


class SubscriptionBase(BaseModel):
    subscription_start: datetime
    subscription_finish: datetime
    count_free_orders: int
    count_orders_available_by_subscription: int
    count_orders_closed_by_subscription: int
    purchase_url: Optional[HttpUrl] = None


class SubscriptionCreate(SubscriptionBase):
    user_uuid: UUID4
    subscription_type_uuid: UUID4


class SubscriptionRead(SubscriptionBase):
    uuid: UUID4
    user_uuid: UUID4
    subscription_type_uuid: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None


class SubscriptionUpdate(BaseModel):
    subscription_start: Optional[datetime] = None
    subscription_finish: Optional[datetime] = None
    count_free_orders: Optional[int] = None
    count_orders_available_by_subscription: Optional[int] = None
    count_orders_closed_by_subscription: Optional[int] = None
    purchase_url: Optional[HttpUrl] = None
