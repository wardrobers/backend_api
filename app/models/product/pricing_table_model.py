from uuid import uuid4
from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from .rental_period_model import RentalPeriod
from ..basemixin import Base


class PricingTable(Base):
    __tablename__ = 'pricing_table'
    
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    base_price = Column(Numeric, nullable=False)
    period_value = Column(Integer)
    price = Column(Numeric, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    product_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('products.uuid'), nullable=False)
    rental_period_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('rental_periods.uuid'), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="price")
    rental_period = relationship("RentalPeriod", back_populates="price")
