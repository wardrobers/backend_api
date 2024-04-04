from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

from ..basemixin import Base


class RentalPeriod(Base):
    __tablename__ = "rental_periods"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    # Assuming there is a Price model that has a foreign key to RentalPeriod
    prices = relationship("Price", back_populates="rental_periods")
