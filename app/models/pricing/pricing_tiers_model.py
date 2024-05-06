from sqlalchemy import Column, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..common.base_model import Base


class PricingTier(Base):
    __tablename__ = "pricing_tiers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    retail_price = Column(Numeric, nullable=False)
    max_price_threshold = Column(Numeric)
    max_price_discount = Column(Numeric)
    tax_percentage = Column(Numeric, nullable=False)
    additional_discount = Column(Numeric)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    product_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False
    )
    category_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.uuid"), nullable=False
    )
    price_multiplier_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("price_multipliers.uuid"), nullable=False
    )

    # Relationships
    price_factors = relationship("PriceFactors", backref="pricing_tiers")
