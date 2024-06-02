from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class PriceMultipliers(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "price_multipliers"

    multiplier = Column(Numeric, nullable=False)

    # Foreign keys
    category_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )

    # Relationships
    pricing_tiers = relationship(
        "app.models.pricing.pricing_tiers_model.PricingTiers",
        backref="price_multipliers",
    )
