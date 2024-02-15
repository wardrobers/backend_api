from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class SubscriptionPeriodBase(BaseModel):
    name: Optional[str]


class SubscriptionPeriodRead(SubscriptionPeriodBase):
    uuid: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


class SubscriptionPeriodCreate(SubscriptionPeriodBase):
    pass


class SubscriptionPeriodUpdate(BaseModel):
    name: Optional[str]
