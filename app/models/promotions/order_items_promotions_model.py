from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models import Base


class OrderItemsPromotions(Base):
    __tablename__ = "order_items_promotions"

    # Foreign Keys
    order_item_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("order_items.id"), nullable=False
    )
    promotions_and_discounts_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("promotions_and_discounts.id"), nullable=False
    )
