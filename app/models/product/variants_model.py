from uuid import uuid4
from sqlalchemy import Column, DateTime, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base


class Variant(Base):
    __tablename__ = "variants"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    eu_size = Column(String)
    index = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    product_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False
    )
    sku_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_keeping_units.uuid"), nullable=True
    )
    name = mapped_column(String, nullable=False)
    color_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("variant_colors.uuid"), nullable=True
    )

    # Relationships
    product = relationship("Product", back_populates="variants")
    sku = relationship("StockKeepingUnit", back_populates="variants")
    color = relationship("VariantColor", back_populates="variants")
