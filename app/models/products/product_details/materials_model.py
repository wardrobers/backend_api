from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models import Base


class Materials(Base):
    __tablename__ = "materials"

    name = Column(String)

    # Foreign Keys
    categories_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products",
        secondary="product_materials",
        backref="materials",
    )


class ProductMaterials(Base):
    __tablename__ = "product_materials"

    percent = Column(Integer)

    # Foreign Keys
    product_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), primary_key=True
    )
    material_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("materials.id"), primary_key=True
    )
