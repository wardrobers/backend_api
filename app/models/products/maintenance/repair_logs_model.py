from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class RepairLogs(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "repair_logs"

    description = Column(Text, nullable=True, comment="Описание")
    cost = Column(Numeric, nullable=True, comment="Цена ремонта")
    repair_date = Column(DateTime, nullable=False, comment="Дата ремонта")

    # Foreign Keys
    article_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("articles.id"),
        nullable=False,
        comment="Индетифекатор",
    )
