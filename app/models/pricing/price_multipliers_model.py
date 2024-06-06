from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base_model import Base


class PriceMultipliers(Base):
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
