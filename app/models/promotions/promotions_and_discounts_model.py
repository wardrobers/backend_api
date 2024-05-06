from sqlalchemy import Column, DateTime, Integer, Numeric, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..common.base_model import Base


class PromotionsAndDiscounts(Base):
    __tablename__ = "promotions_and_discounts"

    uuid = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    code = Column(String, nullable=False, comment="Код")
    description = Column(Text, nullable=True)
    discount_type = Column(String(11), nullable=False, comment="Percentage or fixed")
    discount_value = Column(Numeric, nullable=True)
    max_discount_amount = Column(Numeric, nullable=True)
    valid_from = Column(DateTime, nullable=True)
    valid_to = Column(DateTime, nullable=True)
    max_uses = Column(
        Integer, nullable=True, comment="Number of times this promo can be used"
    )
    uses_left = Column(Integer, nullable=True)
    active = Column(
        Boolean,
        default=True,
        comment="To quickly enable/disable promotions without deleting",
    )
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Relationships for promotions involved in user and product promotions
    user_promotions = relationship("UserPromotions", backref="promotion")
    promotions_products = relationship("PromotionsProducts", backref="promotion")
