from sqlalchemy import Column, DateTime, Table, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


from ..basemixin import Base


class ProductMaterial(Base):
    __tablename__ = "product_materials"
    product_uuid = Column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), primary_key=True
    )
    material_uuid = Column(
        UUID(as_uuid=True), ForeignKey("materials.uuid"), primary_key=True
    )
    percent = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)