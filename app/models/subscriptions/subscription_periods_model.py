from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..common.base_model import Base


class SubscriptionPeriods(Base):
    __tablename__ = "subscription_periods"

    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    name = Column(String, nullable=True, comment="наименование")
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Relationships
    subscription_types = relationship(
        "SubscriptionTypes", backref="subscription_periods"
    )
