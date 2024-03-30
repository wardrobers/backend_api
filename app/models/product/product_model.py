from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from .product_categories_model import product_categories


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    sstatus_code = Column(String, nullable=False)
    product_catalog_uuid = Column(
        UUID(as_uuid=True), ForeignKey("product_catalogs.uuid")
    )
    color_uuid = Column(UUID(as_uuid=True), ForeignKey("colors.uuid"))
    number = Column(String, nullable=False)
    name = Column(String)
    article = Column(String)
    size_uuid = Column(UUID(as_uuid=True), ForeignKey("sizes.uuid"))
    usage_count = Column(Integer, default=0)
    usage_seconds = Column(Integer, default=0)
    factory_number = Column(String)
    base_price = Column(Numeric, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    categories = relationship(
        "Category", secondary=product_categories, back_populates="products"
    )
    materials = relationship(
        "Material", secondary="product_materials", back_populates="products"
    )
    color = relationship("Color", back_populates="products")
    product_catalog = relationship("ProductCatalog", back_populates="products")
    size = relationship("Size", back_populates="products")
