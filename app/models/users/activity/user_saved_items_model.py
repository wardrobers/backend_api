from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class UserSavedItems(Base):
    __tablename__ = "user_saved_items"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    saved_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    user_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    article_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("articles.uuid"), nullable=False
    )
    article = mapped_column(
        String, nullable=False
    )  # Cached article identifier, assuming necessary for performance.
