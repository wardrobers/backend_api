from enum import Enum
from sqlalchemy import Column, DateTime, Integer, Numeric, String, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class DiscountType(Enum):
    Percentage = "Percentage"
    FixedAmount = "FixedAmount"


class PromotionsAndDiscounts(
    Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin
):
    __tablename__ = "promotions_and_discounts"

    code = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    discount_type = Column(SQLAEnum(DiscountType), nullable=False)
    discount_value = Column(Numeric, nullable=True)
    max_discount_amount = Column(Numeric, nullable=True)
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    max_uses = Column(Integer, nullable=True)
    uses_left = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)

    # Relationships for promotions involved in user and product promotions
    user_promotions = relationship("UserPromotions", backref="promotion")
    promotions_products = relationship("PromotionsProducts", backref="promotion")
