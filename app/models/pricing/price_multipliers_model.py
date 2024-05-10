from sqlalchemy import Column, String, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..common.base_model import Base


class PriceMultipliers(Base):
    __tablename__ = "price_multipliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    category = Column(String, nullable=False)
    multiplier = Column(Numeric, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    pricing_tiers = relationship("PricingTiers", backref="price_multipliers")
