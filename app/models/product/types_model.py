from uuid import uuid4
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base


class Type(Base):
    __tablename__ = "types"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    category_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("categories.uuid"))

    # Relationships
    product = relationship("Product", secondary="product_types", back_populates="type")
    category = relationship("Category", back_populates="type")
