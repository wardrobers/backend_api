from enum import Enum

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum

from app.models.base_model import Base


class ArticleCurrentStatus(Enum):
    Available = "Available"
    Rented = "Rented"
    Cleaning = "Cleaning"
    Repair = "Repair"
    Lost = "Lost"
    Damaged = "Damaged"
    Retired = "Retired"


class ArticleStatus(Base):
    __tablename__ = "article_status"

    name = Column(SQLAEnum(ArticleCurrentStatus))

    # Relationships
    article = relationship("Articles", backref="article_status")
