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
    materials = relationship(
        "app.model.products.product_details.materials_model.Materials",
        backref="categories",
    )
    product_categories = relationship(
        "app.models.products.inventorization.categories_model.ProductCategories",
        backref="categories",
    )
    types = relationship(
        "app.models.products.inventorization.types_model.Types", backref="categories"
    )
    pricing_tiers = relationship(
        "app.model.pricing.pricing_tier_model.PricingTier", backref="categories"
    )
    price_multiplier = relationship(
        "app.model.pricing.price_multipliers_model.PriceMultipliers",
        backref="categories",
    )


class ProductCategories(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "product_categories"

    # Foreign Keys
    product_id = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
    category_id = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"))
