from sqlalchemy import Column, DateTime, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


# Many-to-Many relationship helper tables
product_materials = Table(
    "product_materials",
    Base.metadata,
    Column(
        "product_uuid",
        UUID(as_uuid=True),
        ForeignKey("products.uuid"),
        primary_key=True,
    ),
    Column(
        "material_uuid",
        UUID(as_uuid=True),
        ForeignKey("materials.uuid"),
        primary_key=True,
    ),
)


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
