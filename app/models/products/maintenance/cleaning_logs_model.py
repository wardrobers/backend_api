from sqlalchemy import Column, DateTime, Numeric, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class CleaningLogs(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "cleaning_logs"

    article = Column(String, nullable=False)
    description = Column(Text)
    cost = Column(Numeric)
    cleaning_date = Column(DateTime, nullable=False)

    # Foreign keys
    article_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("article.id"), nullable=False
    )
