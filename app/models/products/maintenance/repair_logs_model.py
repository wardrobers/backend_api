from sqlalchemy import Column, DateTime, Numeric, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class RepairLogs(Base):
    __tablename__ = "repair_logs"

    uuid = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    description = Column(Text, nullable=True, comment="Описание")
    cost = Column(Numeric, nullable=True, comment="Цена ремонта")
    repair_date = Column(DateTime, nullable=False, comment="Дата ремонта")
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Foreign Keys
    article_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("article.uuid"),
        nullable=False,
        comment="Индетифекатор",
    )
