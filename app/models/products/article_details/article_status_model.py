from enum import Enum
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class ArticleStatus(Enum):
    Available = "Available"
    Rented = "Rented"
    Cleaning = "Cleaning"
    Repair = "Repair"
    Lost = "Lost"
    Damaged = "Damaged"
    Retired = "Retired"


class ArticleStatus(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "article_status"

    status_code = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    name = Column(SQLAEnum(ArticleStatus))

    # Relationships
    article = relationship("Article", backref="article_status")
