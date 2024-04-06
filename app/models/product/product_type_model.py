from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base


class ProductType(Base):
    __tablename__ = "product_types"
    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    categories = relationship("Category", back_populates="product_type")
    catalog_product_types = relationship("CatalogProductType", back_populates="product_type")