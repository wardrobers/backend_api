from sqlalchemy import Column, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class ProductsCatalogPhoto(Base):
    __tablename__ = "products_catalog_photos"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    products_catalog_uuid = Column(
        UUID(as_uuid=True), ForeignKey("products_catalog.uuid"), nullable=False
    )
    product_uuid = Column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False
    )
    showcase = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=True, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    product = relationship("Product", back_populates="products_catalog_photos")
    products_catalog = relationship("ProductsCatalog", back_populates="photproducts_catalog_photosos")
