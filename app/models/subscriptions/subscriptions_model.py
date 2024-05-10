from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..common.base_model import Base


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    subscription_start = Column(DateTime, nullable=True, comment="Начало подписки")
    subscription_finish = Column(DateTime, nullable=True, comment="Окончание подписки")
    count_free_orders = Column(
        Integer, nullable=True, comment="Кол-во шмоток в подписке"
    )
    count_orders_available_by_subscription = Column(
        Integer, nullable=True, comment="Кол-во заказов доступных по подписке"
    )
    count_orders_closed_by_subscription = Column(
        Integer, nullable=True, comment="Заказы по подписке"
    )
    purchase_url = Column(String, nullable=True, comment="Чек об оплате")
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")

    # Foreign Keys
    user_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        comment="Пользователь",
    )
    subscription_type_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subscription_types.id"),
        nullable=False,
        comment="Тип подписки",
    )
