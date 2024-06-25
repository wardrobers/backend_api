from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field
from typing_extensions import Annotated

from app.schemas.orders import OrderItemRead, TransactionRead

# --- Orders ---


class OrderBase(BaseModel):
    total_price: Annotated[
        Decimal, Field(..., description="The total price of the order.")
    ]
    total_delivery_price: Annotated[
        Decimal,
        Field(..., description="The total delivery price for the order."),
    ]
    comment: Optional[str] = Field(None, description="Any comments for the order.")
    user_id: UUID4 = Field(..., description="The ID of the user who placed the order.")
    status_code: UUID4 = Field(
        ..., description="The ID of the current order status code."
    )


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: UUID4
    transactions: Optional[list[TransactionRead]] = None
    order_items: list[OrderItemRead] = []
    # order_promotions: Optional[List["OrderPromotionRead"]] = None

    class Config:
        from_attributes = True


class OrderUpdate(OrderBase):
    total_price: Optional[
        Annotated[Decimal, Field(description="The total price of the order.")]
    ] = None
    total_delivery_price: Optional[
        Annotated[
            Decimal,
            Field(description="The total delivery price for the order."),
        ]
    ] = None
    comment: Optional[str] = Field(None, description="Any comments for the order.")


# --- Resolving Forward References ---
OrderRead.model_rebuild()
