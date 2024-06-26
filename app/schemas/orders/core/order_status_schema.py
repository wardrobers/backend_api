from typing import Optional

from pydantic import UUID4, BaseModel, Field

from app.schemas.orders.core.orders_schema import OrderRead

# --- Order Status ---


class OrderStatusBase(BaseModel):
    def get_order_status(self):
        from app.models.orders.core.order_status_model import CurrentOrderStatus

        return CurrentOrderStatus

    name: get_order_status = Field(..., description="The current status of the order.")


class OrderStatusCreate(OrderStatusBase):
    pass


class OrderStatusRead(OrderStatusBase):
    id: UUID4
    orders: Optional[list[OrderRead]] = None

    class Config:
        from_attributes = True


class OrderStatusUpdate(OrderStatusBase):
    def get_order_status(self):
        from app.models.orders.core.order_status_model import CurrentOrderStatus

        return CurrentOrderStatus

    name: Optional[get_order_status] = Field(
        None, description="The current status of the order."
    )


# --- Resolving Forward References ---
OrderStatusRead.model_rebuild()
