from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, mapped_column
from sqlalchemy.sql import func
from .product_catalog_model import ProductsCatalog
from .product_catalog_photo_model import ProductsCatalogPhoto

from ..basemixin import Base


class Product(Base):
    __tablename__ = "products"
    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    status_code = Column(String, nullable=False)
    products_catalog_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("products_catalog.uuid")
    )
    color_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("colors.uuid"))
    number = Column(String, nullable=False)
    name = Column(String)
    article = Column(String)
    size_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("sizes.uuid"))
    brand_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("brands.uuid"))
    usage_count = Column(Integer, default=0)
    usage_seconds = Column(Integer, default=0)
    factory_number = Column(String)
    base_price = Column(Numeric, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    materials = relationship("Material", back_populates="products")
    color = relationship("Color", back_populates="products")
    size = relationship("Size", back_populates="products")
    orders = relationship("Order", back_populates="products")
    products_catalog = relationship("ProductsCatalog", back_populates="products")
    price = relationship("Price", back_populates="products")
    products_catalog_photos = relationship("ProductsCatalogPhoto", back_populates="products")
    brand = relationship("Brand", back_populates="products")