from sqlalchemy import ForeignKey, JSON, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class CategoryForUser(Base):
    __tablename__ = "categories_for_user"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    coefficient = Column(String)
    raw = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Foreign keys
    user_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    category_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("categories.uuid"))

    # Relationships
    user = relationship("User", back_populates="category_for_user")
    category = relationship("Category", back_populates="category_for_user")
