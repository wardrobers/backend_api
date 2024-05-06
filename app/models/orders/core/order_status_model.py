from enum import Enum
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.types import Enum as SQLAEnum
from uuid import uuid4

from ...common.base_model import Base


class OrderStatus(Enum):
    Placed = "Placed"
    Confirmed = "Confirmed"
    Processing = "Processing"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Returned = "Returned"
    Cancelled = "Cancelled"


class OrderStatus(Base):
    __tablename__ = "order_status"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(
        SQLAEnum(OrderStatus),
        nullable=False,
        comment="Placed, Confirmed, Processing, Shipped, Delivered, Returned, Cancelled",
    )
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    order = relationship("Order", backref="order_status")
