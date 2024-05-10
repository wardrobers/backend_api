from sqlalchemy import Column, DateTime, Time, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class OrderItems(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "order_items"

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    time_start = Column(Time, nullable=False)
    price = Column(Numeric, nullable=True)
    delivery_price = Column(Numeric, nullable=True)
    comment = Column(Text, nullable=True)

    # Foreign keys
    order_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    article_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("article.id"), nullable=False
    )
    shipping_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("shipping_details.id"), nullable=False
    )

    def __repr__(self):
        return f"<OrderItem(uuid={self.id}, order={self.order_id}, article={self.article_id}, start_date={self.start_date}, end_date={self.end_date})>"
