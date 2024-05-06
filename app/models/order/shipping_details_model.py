from sqlalchemy import Column, ForeignKey, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base

class ShippingDetails(Base):
    __tablename__ = 'shipping_details'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор")
    tracking_number = Column(String, nullable=True)
    shipping_provider = Column(String, nullable=True)
    delivery_status = Column(String(14), nullable=True, comment="e.g., Pending, Shipped, Delivered, Cancelled")
    estimated_delivery_date = Column(DateTime, nullable=True)
    actual_delivery_date = Column(DateTime, nullable=True)
    is_peer_to_peer = Column(Boolean, nullable=True, comment="Доставка от пользователя к пользователю")
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Foreign Keys
    delivery_option_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('delivery_options.uuid'), nullable=False, comment="Тип доставки")
    user_address_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('user_addresses.uuid'), nullable=False, comment="Адрес")