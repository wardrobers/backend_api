from enum import Enum

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class ArticleCurrentStatus(Enum):
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
    name = Column(SQLAEnum(ArticleCurrentStatus))

    # Relationships
    article = relationship("Articles", backref="article_status")
