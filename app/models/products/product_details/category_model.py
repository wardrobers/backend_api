from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
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
    price_multiplier = relationship("PriceMultipliers", backref="categories")


class ProductCategories(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "product_categories"

    # Foreign Keys
    product_id = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
    category_id = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"))
