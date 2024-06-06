from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.repositories.common import Base, BaseMixin


class PriceFactors(Base, BaseMixin):
    __tablename__ = "price_factors"

    rental_period = Column(Numeric, nullable=False)
    percentage = Column(Numeric, nullable=False)

    # Foreign keys
    pricing_tier_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pricing_tiers.id"),
        nullable=False,
    )
