from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref, mapped_column, relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class OrderPromotions(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
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
