from enum import Enum, auto

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base_model import Base


class Products(Base):
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
        "ProductTypes",
        backref="products",
    )
    photos = relationship(
        "ProductPhotos",
        backref="products",
    )
    variants = relationship(
        "Variants", backref="products"
    )
    user_reviews_and_ratings = relationship(
        "UserReviewsAndRatings",
        backref="products",
    )
    categories = relationship(
        "ProductCategories",
        backref="products",
    )
    occasional_categories = relationship(
        "ProductOccasionalCategories",
        backref="products",
        lazy="joined",  # Eager load for improved performance
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}'')>"
