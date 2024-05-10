from sqlalchemy import Column, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class RepairLogs(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "repair_logs"

    description = Column(Text, nullable=True, comment="Описание")
    cost = Column(Numeric, nullable=True, comment="Цена ремонта")
    repair_date = Column(DateTime, nullable=False, comment="Дата ремонта")

    # Foreign Keys
    article_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("article.id"),
        nullable=False,
        comment="Индетифекатор",
    )
