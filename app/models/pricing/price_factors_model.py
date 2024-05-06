from sqlalchemy import Column, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..common.base_model import Base


class PriceFactors(Base):
    __tablename__ = "price_factors"

    uuid = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    rental_period = Column(Numeric, nullable=False, comment="Rental period")
    percentage = Column(
        Numeric, nullable=False, comment="Percentage of the price for the period"
    )
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")
    deleted_at = Column(DateTime, comment="Удалено")

    # Foreign keys
    pricing_tier_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pricing_tiers.uuid"),
        nullable=False,
        comment="Индетифекатор",
    )
