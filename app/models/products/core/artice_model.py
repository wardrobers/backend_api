from enum import Enum
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum
from uuid import uuid4

from ...common.base_model import Base


class OwnerType(Enum):
    Platform = "Platform"
    Lender = "Lender"
    Brand = "Brand"
    Partner = "Partner"


class Condition(Enum):
    New = "New"
    Excellent = "Excellent"
    Good = "Good"
    Fair = "Fair"
    Poor = "Poor"


class Article(Base):
    __tablename__ = "article"

    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    article = Column(String, nullable=False, comment="Артикул")
    sku_article = Column(
        String, nullable=False, comment="Артикул для каждой уникальной вещи"
    )
    owner_type = Column(
        SQLAEnum(OwnerType), nullable=False, comment="Platform, Lender, Brand, Partner"
    )
    factory_number = Column(String, nullable=True, comment="Заводской номер")
    times_used = Column(
        Integer, nullable=False, default=0, comment="Кол-во использованей"
    )
    hours_used = Column(
        Integer, nullable=False, default=0, comment="Часов в использование"
    )
    min_rental_days = Column(
        Integer, nullable=False, default=2, comment="Минимальная аренда в днях"
    )
    buffer_days = Column(
        Integer, nullable=False, default=1, comment="Дней на обслуживание после заказа"
    )
    pre_rental_buffer = Column(Integer, nullable=True, default=0)
    for_cleaning = Column(
        Boolean, nullable=True, default=False, comment="Требуется чистка?"
    )
    for_repair = Column(
        Boolean, nullable=True, default=False, comment="Требуется ремонт?"
    )
    condition = Column(
        SQLAEnum(Condition), nullable=False, comment="Описание состояния"
    )
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="Создано")
    updated_at = Column(
        DateTime, nullable=True, onupdate=func.now(), comment="Отредактировано"
    )
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Foreign keys
    sku_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stock_keeping_unit.uuid"),
        nullable=False,
        comment="Индетифекатор",
    )
    status_code = mapped_column(
        String,
        ForeignKey("article_status.status_code"),
        nullable=False,
        comment="Статус",
    )
    types_of_operation_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("types_of_operations.uuid"),
        nullable=False,
        comment="Тип операций",
    )

    # Relationships
    specification = relationship("Specificatios", backref="article")
    cleaning_logs = relationship("CleaningLogs", backref="article")
    repair_logs = relationship("RepairLogs", backref="article")
    lender_payments = relationship("LenderPayments", backref="article")
    user_saved_items = relationship("UserSavedItems", backref="article")
