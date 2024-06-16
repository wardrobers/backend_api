from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Text, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base_model import Base
from app.models.promotions.order_items_promotions_model import OrderItemsPromotions


class OrderItems(Base):
    __tablename__ = "order_items"

    start_date = Column(DateTime)
    end_date = Column(DateTime)
    time_start = Column(Time)
    price = Column(Numeric)
    delivery_price = Column(Numeric, nullable=True)
    comment = Column(Text, nullable=True)

    # Foreign keys
    order_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    article_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False
    )
    shipping_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("shipping_details.id"), nullable=False
    )

    # Relationships
    promotions = relationship(
        "OrderItemsPromotions",
        backref="order_items",
        lazy="joined",
        cascade="all, delete-orphan",
    )
    peer_to_peer = relationship(
        "PeerToPeerLogistics",
        backref="order_items",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<OrderItems(id={self.id}, order={self.order_id}, article={self.article_id}, start_date={self.start_date}, end_date={self.end_date})>"
