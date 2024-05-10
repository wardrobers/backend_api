from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum
from uuid import uuid4

from ...common.base_model import Base


class PaymentStatus(Enum):
    Pending = "Pending"
    Paid = "Paid"
    Failed = "Failed"
    Processing = "Processing"
    Refunded = "Refunded"


class LenderPayments(Base):
    __tablename__ = "lender_payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    payment_percentage = Column(Integer, nullable=False)
    payment_amount = Column(Numeric, nullable=False)
    payment_status = Column(SQLAEnum(PaymentStatus))
    updated_at = Column(DateTime, onupdate=func.now())
    created_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    article_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("article.id"), nullable=False
    )
    transaction_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False
    )
