from pydantic import BaseModel, UUID4, Field
from datetime import datetime

from ..user.user_schema import UserRead
from ..product.product_schema import ProductRead


class OrderBase(BaseModel):
    start: datetime
    end: datetime
    price: float


class OrderCreate(OrderBase):
    user_uuid: UUID4
    product_uuid: UUID4


class OrderRead(OrderBase):
    uuid: UUID4
    user: UserRead
    product: ProductRead

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    start: datetime = Field(None)
    end: datetime = Field(None)
    price: float = Field(None)
