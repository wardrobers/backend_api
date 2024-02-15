from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID as UUIDType
from datetime import datetime


class RentalPeriodBase(BaseModel):
    uuid: Optional[UUIDType] = Field(default_factory=UUIDType)
    name: Optional[str] = None


class RentalPeriodCreate(RentalPeriodBase):
    pass


class RentalPeriodRead(RentalPeriodBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
