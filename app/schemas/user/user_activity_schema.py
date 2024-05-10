from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class UserActivityBase(BaseModel):
    user_id: UUID4
    total_confirmed_orders: int = 0
    total_canceled_orders: int = 0
    activity_orders: int = 0
    subscription_now: bool = False
    total_money_spent: Optional[float] = (
        None  # Using float for simplicity in JSON serialization
    )


class UserActivityCreate(UserActivityBase):
    pass  # Inherits all attributes from UserActivityBase


class UserActivityRead(BaseModel):
    uuid: UUID4
    user_id: UUID4
    total_confirmed_orders: int
    total_canceled_orders: int
    activity_orders: int
    subscription_now: bool
    total_money_spent: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserActivityUpdate(BaseModel):
    total_confirmed_orders: Optional[int] = None
    total_canceled_orders: Optional[int] = None
    activity_orders: Optional[int] = None
    subscription_now: Optional[bool] = None
    total_money_spent: Optional[float] = None
