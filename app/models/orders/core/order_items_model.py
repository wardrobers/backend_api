from sqlalchemy import Column, DateTime, Time, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class OrderItems(Base):
    __tablename__ = "order_items"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    time_start = Column(Time, nullable=False)
    price = Column(Numeric, nullable=True)
    delivery_price = Column(Numeric, nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Foreign keys
    order_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.uuid"), nullable=False
    )
    article_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("article.uuid"), nullable=False
    )
    shipping_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("shipping_details.uuid"), nullable=False
    )

    def __repr__(self):
        return f"<OrderItem(uuid={self.uuid}, order={self.order_uuid}, article={self.article_uuid}, start_date={self.start_date}, end_date={self.end_date})>"
