from enum import Enum
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum
from uuid import uuid4

from ...common.base_model import Base


class ArticleStatus(Enum):
    Available = "Available"
    Rented = "Rented"
    Cleaning = "Cleaning"
    Repair = "Repair"
    Lost = "Lost"
    Damaged = "Damaged"
    Retired = "Retired"


class ArticleStatus(Base):
    __tablename__ = "article_status"

    status_code = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(SQLAEnum(ArticleStatus))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    article = relationship("Article", backref="article_status")
