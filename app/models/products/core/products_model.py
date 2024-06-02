from enum import Enum, auto

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class Products(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "products"

    name = Column(String, nullable=False)
    description = Column(Text)
    instructions = Column(String)

    # Foreign Keys
    brand_id = mapped_column(UUID(as_uuid=True), ForeignKey("brands.id"))
    clothing_size_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("clothing_sizes.id")
    )
    clasp_type_id = mapped_column(UUID(as_uuid=True), ForeignKey("clasp_types.id"))
    size_and_fit_id = mapped_column(UUID(as_uuid=True), ForeignKey("product_fit.id"))
    status_code = mapped_column(String, ForeignKey("product_status.code"))
    accessories_size_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("accessories_size.id"), nullable=False
    )

    # Relationships
    types = relationship(
        "app.models.products.inventorization.types_model.ProductTypes",
        backref="products",
    )
    photos = relationship(
        "app.models.products.product_details.product_photos_model.ProductPhotos",
        backref="products",
    )
    variants = relationship(
        "app.models.products.core.variants_model.Variants", backref="products"
    )
    user_reviews_and_ratings = relationship(
        "app.models.users.activity.user_reviews_and_ratings_model.UserReviewsAndRatings",
        backref="products",
    )
    categories = relationship(
        "app.models.products.inventorization.categories_model.ProductCategories",
        backref="products",
    )
    promotions_products = relationship(
        "app.models.promotions.promotions_variants_model.PromotionsVariants",
        backref="products",
    )
    occasional_categories = relationship(
        "app.models.products.inventorization.occasional_categories_model.ProductOccasionalCategories",
        backref="products",
        lazy="joined",  # Eager load for improved performance
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}'')>"
