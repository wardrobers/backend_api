from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func


from ...common.base_model import Base


class ProductMaterials(Base):
    __tablename__ = "product_materials"

    percent = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    product_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), primary_key=True
    )
    material_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("materials.uuid"), primary_key=True
    )