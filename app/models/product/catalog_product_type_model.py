from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()


class CatalogProductType(Base):
    __tablename__ = "catalog_product_types"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    product_type_uuid = Column(
        UUID(as_uuid=True), ForeignKey("product_types.uuid"), nullable=False
    )
    product_catalog_uuid = Column(
        UUID(as_uuid=True), ForeignKey("products_catalog.uuid"), nullable=False
    )
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    product_type = relationship("ProductType", back_populates="catalogs")
    product_catalog = relationship("ProductCatalog", back_populates="product_types")
