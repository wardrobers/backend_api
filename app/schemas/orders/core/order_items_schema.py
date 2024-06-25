from datetime import datetime, time
from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field
from typing_extensions import Annotated

# --- Order Items ---


class OrderItemBase(BaseModel):
    start_date: datetime = Field(
        ..., description="The start date of the rental period."
    )
    end_date: datetime = Field(..., description="The end date of the rental period.")
    time_start: Optional[time] = Field(
        None, description="Time of day for rental start."
    )
    price: Annotated[
        Decimal, Field(..., description="The rental price of the article.")
    ]
    delivery_price: Optional[
        Annotated[Decimal, Field(description="The delivery price for the article.")]
    ] = None
    comment: Optional[str] = Field(None, description="Any comment for the order item.")
    order_id: UUID4 = Field(
        ..., description="The ID of the order this item belongs to."
    )
    article_id: UUID4 = Field(..., description="The ID of the article being rented.")
    shipping_id: UUID4 = Field(
        ..., description="The ID of the shipping details for this item."
    )


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: UUID4
    # promotions: Optional[list["OrderItemPromotionRead"]] = None
    # peer_to_peer: Optional["PeerToPeerLogisticsRead"] = None

    class Config:
        from_attributes = True


class OrderItemUpdate(OrderItemBase):
    start_date: Optional[datetime] = Field(
        None, description="The start date of the rental period."
    )
    end_date: Optional[datetime] = Field(
        None, description="The end date of the rental period."
    )
    time_start: Optional[time] = Field(
        None, description="Time of day for rental start."
    )
    price: Optional[
        Annotated[Decimal, Field(description="The rental price of the article.")]
    ] = None
    delivery_price: Optional[
        Annotated[Decimal, Field(description="The delivery price for the article.")]
    ] = None
    comment: Optional[str] = Field(None, description="Any comment for the order item.")


# --- Resolving Forward References ---
OrderItemRead.model_rebuild()
