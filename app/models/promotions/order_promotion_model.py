from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, backref
from sqlalchemy.sql import func
from uuid import uuid4

from ..common.base_model import Base


class OrderPromotions(Base):
    __tablename__ = "order_promotions"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    order_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.uuid"), nullable=False
    )
    promotion_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("promotions_and_discounts.uuid"), nullable=False
    )

    # Relationships
    order = relationship("Order", backref=backref("order_promotions", uselist=True))
    promotion = relationship(
        "Promotion", backref=backref("order_promotions", uselist=True)
    )
