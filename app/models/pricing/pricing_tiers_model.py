from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class PricingTier(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "pricing_tiers"

    retail_price = Column(Numeric, nullable=False)
    max_price_threshold = Column(Numeric)
    max_price_discount = Column(Numeric)
    additional_discount = Column(Numeric)
    tax_percentage = Column(Numeric, nullable=False)
    insurance = Column(Numeric)
    cleaning = Column(Numeric)

    # Foreign keys
    product_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    category_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    price_multiplier_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("price_multipliers.id"), nullable=False
    )

    # Relationships
    price_factors = relationship("PriceFactors", backref="pricing_tiers")
