from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class Orders(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
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
    transactions = relationship(
        "app.model.orders.payments.transactions_model.Transactions", backref="orders"
    )
    order_items = relationship(
        "app.model.orders.core.order_items_model.OrderItems", backref="orders"
    )
