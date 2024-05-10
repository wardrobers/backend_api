from enum import Enum
from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum
from uuid import uuid4

from ...common.base_model import Base


class AddressType(Enum):
    Shipping = "Shipping"
    Billing = "Billing"
    Both = "Both"


class UserAddresses(Base):
    __tablename__ = "user_addresses"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    address_line1 = Column(String, nullable=True, comment="Улица, номер дома")
    address_line2 = Column(String, nullable=True, comment="Номер квартиры/офиса")
    city = Column(String, nullable=True, comment="Город")
    country = Column(String, nullable=True, comment="Страна")
    postal_code = Column(String, nullable=True, comment="Индекс")
    address_type = Column(
        SQLAEnum(AddressType), nullable=True, comment="Shipping, Billing, Both"
    )
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Foreign Keys
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        comment="Пользователь",
    )

    # Relationships
    shipping_details = relationship("ShippingDetails", back_populates="user_addresses")
    transactions = relationship("Transactions", back_populates="user_addresses")
