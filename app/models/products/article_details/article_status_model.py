from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class ArticleStatus(Base):
    __tablename__ = "article_status"

    status_code = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(9))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    article = relationship("Article", backref="article_status")
