from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class PriceMultipliers(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "price_multipliers"

    category = Column(String, nullable=False)
    multiplier = Column(Numeric, nullable=False)

    # Relationships
    pricing_tiers = relationship("PricingTiers", backref="price_multipliers")
