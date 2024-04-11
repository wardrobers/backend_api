from sqlalchemy import Column, DateTime, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from .product_materials_model import ProductMaterial
from ..basemixin import Base


class Product(Base):
    __tablename__ = "products"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    instructions = Column(String)
    size = Column(String)
    boot_height = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    brand_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("brands.uuid"))
    product_status_code = mapped_column(
        UUID(as_uuid=True), ForeignKey("product_status.code")
    )
    tax_percentage_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("tax_percentage.uuid")
    )
    clothing_size_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("clothing_sizes.uuid")
    )
    clasp_type_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("clasp_types.uuid"))

    # Relationships
    brand = relationship("Brand", back_populates="product")
    product_status = relationship("ProductStatus", back_populates="product")
    tax_percentage = relationship("TaxPercentage", back_populates="product")
    clothing_size = relationship("ClothingSize", back_populates="product")
    clasp_type = relationship("ClaspType", back_populates="product")
    variant = relationship("Variant", back_populates="product")
    type = relationship("Type", back_populates="product")
    size_and_fit = relationship("SizeAndFit", back_populates="product")
    clothing_size = relationship("ClothingSize", back_populates="product")
    price = relationship("PricingTable", back_populates="product")
    clasp_type = relationship("ClaspType", back_populates="product")
    material = relationship(
        "Material", secondary="product_materials", back_populates="product"
    )
