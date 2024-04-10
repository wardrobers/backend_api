from sqlalchemy import Column, DateTime, String, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from .product_catalog_model import ProductsCatalog
from .product_catalog_photo_model import ProductsCatalogPhoto
from .product_material_model import ProductMaterial
from ..basemixin import Base


class Product(Base):
    __tablename__ = "products"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    status_code = Column(UUID(as_uuid=True), unique=True, nullable=False)
    description = Column(String)
    instructions = Column(String)
    size = Column(String)
    boot_height = Column(Numeric)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    brand_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('brands.uuid'), nullable=False)

    # Relationships
    materials = relationship("Material", secondary="product_materials", back_populates="product")
    color = relationship("Color", back_populates="product")
    size = relationship("Size", back_populates="product")
    orders = relationship("Order", back_populates="product")
    products_catalog = relationship("ProductsCatalog", back_populates="product")
    price = relationship("Price", back_populates="product")
    products_catalog_photos = relationship("ProductsCatalogPhoto", back_populates="product")
    brand = relationship("Brand", back_populates="product")