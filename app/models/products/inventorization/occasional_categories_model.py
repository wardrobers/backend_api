from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base_model import Base


class OccasionalCategories(Base):
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


class ProductOccasionalCategories(Base):
    __tablename__ = "product_occasional_categories"

    # Foreign Keys
    product_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    occasional_category_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("occasional_categories.id"), nullable=False
    )
