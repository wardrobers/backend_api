from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class Categories(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "categories"

    name = Column(String)
    is_default = Column(Boolean)

    # Relationships
    materials = relationship("Materials", backref="categories")
    product_categories = relationship("ProductCategories", backref="categories")
    categories_for_user = relationship("CategoriesForUser", backref="categories")
    types = relationship("Types", backref="categories")
    pricing_tiers = relationship("PricingTier", backref="categories")
