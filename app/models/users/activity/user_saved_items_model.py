from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.repositories.common import Base, BaseMixin


class UserSavedItems(Base, BaseMixin):
    __tablename__ = "user_saved_items"

    saved_at = Column(DateTime, default=func.now())

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    article_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False
    )
    article = mapped_column(String, nullable=False)
