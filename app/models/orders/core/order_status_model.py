from enum import Enum

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.base_model import Base


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

    name = Column(
        SQLAEnum(OrderStatus),
        nullable=False,
    )

    # Relationships
    order = relationship(
        "app.models.orders.Orders", backref="order_status"
    )
