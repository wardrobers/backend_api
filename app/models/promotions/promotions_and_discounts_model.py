from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin
from app.models.promotions import PromotionsOccasionalCategories, PromotionsVariants


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

    # Relationships
    user_promotions = relationship("UserPromotions", backref="promotions_and_discounts")
    promotions_variants = relationship(
        "PromotionsVariants", backref="promotions_and_discounts"
    )
    occasional_categories = relationship(
        "PromotionsOccasionalCategories", backref="promotion", lazy="dynamic"
    )
    variants = relationship("PromotionsVariants", backref="promotion", lazy="dynamic")

    def is_applicable_to_product(self, product, db_session) -> bool:
        """
        Checks if the promotion is applicable to a given product based on associated categories and variants.
        """
        # Check if the promotion is linked to any of the product's occasional categories
        for product_oc in product.occasional_categories:
            if (
                db_session.query(PromotionsOccasionalCategories)
                .filter(
                    PromotionsOccasionalCategories.occasional_category_id
                    == product_oc.occasional_category_id,
                    PromotionsOccasionalCategories.promotions_and_discounts_id
                    == self.id,
                )
                .first()
            ):
                return True

        # Check if the promotion is linked to any of the product's variants
        for variant in product.variants:
            if (
                db_session.query(PromotionsVariants)
                .filter(
                    PromotionsVariants.variants_id == variant.id,
                    PromotionsVariants.promotions_and_discounts_id == self.id,
                )
                .first()
            ):
                return True

        return False
