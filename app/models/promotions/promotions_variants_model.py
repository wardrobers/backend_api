from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class PromotionsVariants(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "promotions_variants"

    # Foreign Keys
    variant_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("variants.id"), nullable=False
    )
    promotion_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("promotions_and_discounts.id"), nullable=False
    )
