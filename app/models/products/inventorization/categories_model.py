from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base_model import Base


class Categories(Base):
    __tablename__ = "categories"

    name = Column(String, nullable=False)
    is_default = Column(Boolean, nullable=False)

    # Relationships
    materials = relationship(
        "Materials",
        backref="categories",
    )
    product_categories = relationship(
        "ProductCategories",
        backref="categories",
        cascade="all, delete-orphan",
    )
    types = relationship("Types", backref="categories")
    price_multiplier = relationship(
        "PriceMultipliers",
        backref="categories",
    )


class ProductCategories(Base):
    __tablename__ = "product_categories"

    # Foreign Keys
    product_id = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
    category_id = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"))
