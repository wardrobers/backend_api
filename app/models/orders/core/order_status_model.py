from enum import Enum

from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class OrderStatus(Enum):
    Placed = "Placed"
    Confirmed = "Confirmed"
    Processing = "Processing"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Returned = "Returned"
    Cancelled = "Cancelled"


class OrderStatus(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "order_status"

    name = Column(
        SQLAEnum(OrderStatus),
        nullable=False,
    )

    # Relationships
    order = relationship(
        "app.model.orders.core.order_model.Orders", backref="order_status"
    )
