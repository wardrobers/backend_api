from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class Materials(Base):
    __tablename__ = "materials"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    categories_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.uuid"), nullable=False
    )

    # Relationships
    product = relationship(
        "Product", secondary="product_materials", backref="materials"
    )