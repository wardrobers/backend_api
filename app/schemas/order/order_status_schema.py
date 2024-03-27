from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class OrderStatusBase(BaseModel):
    code: str
    name: str


# For reading order status data, including all fields and UUID
class OrderStatusRead(OrderStatusBase):
    uuid: UUID4
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# For creating a new order status, omitting auto-generated fields
class OrderStatusCreate(OrderStatusBase):
    pass


# For updating an existing order status, allowing optional updates to each field
class OrderStatusUpdate(BaseModel):
    code: Optional[str]
    name: Optional[str]
