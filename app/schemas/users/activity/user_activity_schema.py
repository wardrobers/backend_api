from typing import Optional

from pydantic import UUID4, BaseModel


class UserActivityBase(BaseModel):
    total_confirmed_orders: int = 0
    total_canceled_orders: int = 0
    activity_orders: int = 0
    subscription_now: bool = False
    total_money_spent: Optional[float] = None


class UserActivityRead(UserActivityBase):
    id: UUID4
    user_id: UUID4
