from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class DeliveryStatus(Enum):
    Pending = "Pending"
    Shipped = "Shipped"
    InTransit = "InTransit"
    OutForDelivery = "OutForDelivery"
    Delivered = "Delivered"
    Cancelled = "Cancelled"
    Returned = "Returned"


class ShippingDetails(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "shipping_details"

    tracking_number = Column(String, nullable=True)
    shipping_provider = Column(String, nullable=True)
    delivery_status = Column(SQLAEnum(DeliveryStatus), nullable=True)
    estimated_delivery_date = Column(DateTime, nullable=True)
    actual_delivery_date = Column(DateTime, nullable=True)
    is_peer_to_peer = Column(Boolean, nullable=True)

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
        "app.model.orders.core.order_items_model.OrderItems",
        back_populates="shipping_details",
    )
