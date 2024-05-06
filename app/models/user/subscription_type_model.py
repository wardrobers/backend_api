from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class SubscriptionTypes(Base):
    __tablename__ = "subscription_types"

    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    name = Column(String, nullable=True, comment="наименование")
    price = Column(Numeric, nullable=False, comment="Цена")
    count_free_orders = Column(
        Integer, nullable=False, comment="Кол-во шмоток в подписке"
    )
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")
    deleted_at = Column(DateTime, nullable=True, comment="Удалено (?)")

    # Foreign Keys
    period_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subscription_periods.uuid"),
        nullable=False,
        comment="Период",
    )

    # Relationships
    subscriptions = relationship("Subscriptions", backref="subscription_types")
