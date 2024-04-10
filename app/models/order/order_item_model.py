from sqlalchemy import Column, DateTime, Time, ForeignKey, String, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    time_start = Column(Time, nullable=False)
    price = Column(Numeric)
    comment = Column(Text)
    bill = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    order_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('orders.uuid'), nullable=False)
    article_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('article.uuid'), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="order_item")
    article = relationship("Article", back_populates="order_item")
