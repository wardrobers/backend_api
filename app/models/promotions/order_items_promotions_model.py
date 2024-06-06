from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.repositories.common import Base, BaseMixin


class OrderItemsPromotions(Base, BaseMixin):
    __tablename__ = "order_items_promotions"

    # Foreign Keys
    order_item_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("order_items.id"), nullable=False
    )
    promotions_and_discounts_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("promotions_and_discounts.id"), nullable=False
    )
