from sqlalchemy import Column, DateTime, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4


from ...common.base_model import Base


class UserActivity(Base):
    __tablename__ = "user_activity"

    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    total_confirmed_orders = Column(
        Integer, nullable=False, default=0, comment="Кол-во заказов"
    )
    total_canceled_orders = Column(
        Integer, nullable=False, default=0, comment="Отмененные заказы"
    )
    activity_orders = Column(
        Integer, nullable=False, default=0, comment="активные заказы"
    )
    subscription_now = Column(
        Boolean, nullable=False, default=False, comment="Подписка"
    )
    total_money_spent = Column(Numeric, nullable=True, comment="Потрачено денег")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="Создано")
    updated_at = Column(
        DateTime, nullable=True, onupdate=func.now(), comment="Отредактировано"
    )

    # Foreign Keys
    user_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid"),
        nullable=False,
        comment="Пользователь",
    )
