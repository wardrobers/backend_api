from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class Order(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "orders"

    total_price = Column(Numeric, nullable=False)
    total_delivery_price = Column(Numeric, nullable=False)
    comment = Column(String, nullable=True)

    # Foreign keys
    user_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    status_code = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("order_status.id"),
        nullable=False,
    )

    # Relationships
    transactions = relationship("Transactions", backref="orders")
    order_items = relationship("OrderItems", backref="orders")
