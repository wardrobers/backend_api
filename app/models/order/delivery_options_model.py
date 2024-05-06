
from sqlalchemy import Column, Numeric, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class DeliveryOptions(Base):
    __tablename__ = 'delivery_options'
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, comment='Индетифекатор')
    name = Column(String, nullable=False, comment='e.g., Standard, Express, Uber Delivery')
    cost = Column(Numeric, nullable=True, comment='Стоимость доставки')
    active = Column(Boolean, default=True, comment='Активен ли метод')
    created_at = Column(DateTime, default=func.now(), comment='Создано')
    updated_at = Column(DateTime, onupdate=func.now(), comment='Отредактировано')
    deleted_at = Column(DateTime, comment='Удалено')