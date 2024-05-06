from sqlalchemy import Column, ForeignKey, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4


from ...common.base_model import Base


class Order(Base):
    __tablename__ = "orders"

    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    total_price = Column(Numeric, nullable=False, comment="Цена за заказ")
    total_delivery_price = Column(Numeric, nullable=False, comment="Цена за доставку")
    comment = Column(String, nullable=True, comment="Коммент")
    created_at = Column(DateTime, nullable=True, default=func.now(), comment="Создано")
    updated_at = Column(
        DateTime, nullable=True, onupdate=func.now(), comment="Отредактировано"
    )
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Foreign keys
    user_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid"),
        nullable=False,
        comment="Пользователь",
    )
    status_code = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("order_status.uuid"),
        nullable=False,
        comment="Статус",
    )

    # Relationships
    transactions = relationship("Transactions", backref="orders")
    order_items = relationship("OrderItems", backref="orders")
