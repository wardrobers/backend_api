from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, mapped_column, relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.base_model import Base
from app.models.orders.core.order_items_model import OrderItems


class DeliveryStatus(Enum):
    Pending = "Pending"
    Shipped = "Shipped"
    InTransit = "InTransit"
    OutForDelivery = "OutForDelivery"
    Delivered = "Delivered"
    Cancelled = "Cancelled"
    Returned = "Returned"


class ShippingDetails(Base):
    __tablename__ = "shipping_details"

    tracking_number = Column(String)
    shipping_provider = Column(String, nullable=True)
    delivery_status = Column(SQLAEnum(DeliveryStatus))
    estimated_delivery_date = Column(DateTime, nullable=True)
    actual_delivery_date = Column(DateTime)
    is_peer_to_peer = Column(Boolean)

    # Foreign Keys
    delivery_option_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("delivery_options.id"),
        nullable=False,
    )
    user_address_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_addresses.id"),
        nullable=False,
    )

    # Relationships
    order_items = relationship(
        "OrderItems",
        backref="shipping_details",
        cascade="all, delete-orphan",
    )
    peer_to_peer = relationship(
        "PeerToPeerLogistics",
        backref="shipping_details",
        cascade="all, delete-orphan",
    )
