from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, mapped_column, relationship

from app.repositories.common import Base, BaseMixin


class OrderPromotions(Base, BaseMixin):
    __tablename__ = "order_promotions"

    # Foreign Keys
    order_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    promotion_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("promotions_and_discounts.id"), nullable=False
    )

    # Relationships
    order = relationship("Orders", backref=backref("order_promotions", uselist=True))
    promotion = relationship(
        "Promotion", backref=backref("order_promotions", uselist=True)
    )
