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


class PromotionsOccasionalCategories(
    Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin
):
    __tablename__ = "promotions_occasional_categories"

    # Foreign Keys
    occasional_category_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("occasional_categories.id"), nullable=False
    )
    promotions_and_discounts_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("promotions_and_discounts.id"), nullable=False
    )
