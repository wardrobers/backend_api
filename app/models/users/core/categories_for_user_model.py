from sqlalchemy import ForeignKey, JSON, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class CategoriesForUser(Base):
    __tablename__ = "categories_for_user"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    coefficient = Column(String)
    raw = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Foreign keys
    user_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    category_id = mapped_column(UUID(as_uuid=True), ForeignKey("types.id"))
