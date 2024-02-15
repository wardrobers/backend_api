from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime

from .rental_period_schema import RentalPeriodBase


class RentalPeriodBase(BaseModel):
    uuid: UUID4
    name: str
    created_at: datetime
    updated_at: Optional[datetime]

class PriceBase(BaseModel):
    uuid: Optional[UUID4] = Field(default_factory=UUID4)
    product_uuid: UUID4
    time_period_uuid: UUID4
    time_value: int
    price: float
    created_at: datetime
    updated_at: Optional[datetime]

class PriceCreate(PriceBase):
    pass

class PriceRead(PriceBase):
    rental_period: Optional[RentalPeriodBase]

    class Config:
        orm_mode = True
