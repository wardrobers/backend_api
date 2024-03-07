from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime

from .rental_period_schema import RentalPeriodBase


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


class PriceUpdate(BaseModel):
    product_uuid: Optional[UUID4] = Field(
        None, description="The UUID of the associated product."
    )
    time_period_uuid: Optional[UUID4] = Field(
        None, description="The UUID of the associated rental period."
    )
    time_value: Optional[int] = Field(
        None, description="The time value associated with this price."
    )
    price: Optional[float] = Field(
        None, description="The actual price for the given time period."
    )

    class Config:
        schema_extra = {
            "example": {
                "product_uuid": "123e4567-e89b-12d3-a456-426614174000",
                "time_period_uuid": "123e4567-e89b-12d3-a456-426614174001",
                "time_value": 30,
                "price": 15.99,
            }
        }
