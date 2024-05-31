from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)

# from app.models.products.core import Products


class OccasionalCategories(
    Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin
):
    __tablename__ = "occasional_categories"

    name = Column(String, nullable=False)
    img_url = Column(String, nullable=False)

    # Relationships
    product_occasional_categories = relationship(
        "ProductOccasionalCategories", backref="occasional_categories"
    )
    promotions_occasional_categories = relationship(
        "PromotionsOccasionalCategories", backref="occasional_categories"
    )
    products = relationship(
        "Products",
        secondary="product_occasional_categories",
        backref="occasional_categories",
    )

    # def get_product_count(self, db_session):
    #     """Returns the number of active products associated with this occasional category."""
    #     return (
    #         db_session.query(Products)
    #         .join(ProductOccasionalCategories)
    #         .filter(
    #             ProductOccasionalCategories.occasional_category_id == self.id,
    #             Products.deleted_at.is_(None),
    #         )
    #         .count()
    #     )


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
