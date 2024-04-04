from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from ..basemixin import Base


class Price(Base):
    __tablename__ = "prices"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    product_uuid = Column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False
    )
    time_period_uuid = Column(
        UUID(as_uuid=True), ForeignKey("rental_periods.uuid"), nullable=False
    )
    time_value = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    product = relationship("Product", back_populates="prices")
    rental_period = relationship("RentalPeriod", back_populates="prices")
