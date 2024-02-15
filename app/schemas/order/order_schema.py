from pydantic import BaseModel, UUID4
from datetime import datetime


class OrderBase(BaseModel):
    start: datetime
    end: datetime
    price: float


class OrderRead(OrderBase):
    uuid: UUID4
    user: UserRead
    product: ProductRead


class OrderCreate(OrderBase):
    user_uuid: UUID4
    product_uuid: UUID4
