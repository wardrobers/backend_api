from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, mapped_column
from sqlalchemy.sql import func


from ..basemixin import Base


class ProductsCatalog(Base):
    __tablename__ = "products_catalog"
    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    brand_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("brands.uuid"))
    name = Column(String)
    description = Column(String)
    instructions = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    products = relationship("Product", back_populates="products_catalog")
    catalog_product_types = relationship("Product", back_populates="products_catalog")