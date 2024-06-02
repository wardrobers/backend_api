from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class OccasionalCategories(
    Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin
):
    __tablename__ = "occasional_categories"

    name = Column(String, nullable=False)
    img_url = Column(String, nullable=False)

    # Relationships
    product_occasional_categories = relationship(
        "app.models.products.inventorization.products_occasional_categories_model.ProductOccasionalCategories",
        backref="occasional_categories",
    )
    promotions_occasional_categories = relationship(
        "app.models.promotions.promotions_occasional_categories_model.PromotionsOccasionalCategories",
        backref="occasional_categories",
    )
    products = relationship(
        "app.models.products.core.products_model.Products",
        secondary="product_occasional_categories",
        backref="occasional_categories",
    )


class ProductOccasionalCategories(
    Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin
):
    __tablename__ = "product_occasional_categories"

    # Foreign Keys
    product_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    occasional_category_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("occasional_categories.id"), nullable=False
    )
