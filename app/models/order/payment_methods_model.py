from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class PaymentMethods(Base):
    __tablename__ = "payment_methods"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(12))
    provider = Column(String(9))
    card_hash = Column(BYTEA)
    token = Column(String)
    exp_month = Column(Integer)
    exp_year = Column(Integer)
    lender = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    transactions = relationship("Transactions", back_populates="payment_method")
