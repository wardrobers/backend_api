from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class Category(Base):
    __tablename__ = "categories"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    is_default = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    type = relationship("Type", back_populates="category")
    material = relationship("Material", back_populates="category")
    category_for_user = relationship("CategoryForUser", back_populates="category")
    product_categories = relationship("ProductCategories", back_populates="category")
