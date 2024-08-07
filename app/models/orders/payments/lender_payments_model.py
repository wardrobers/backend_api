from enum import Enum
from sqlalchemy import Column, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class PaymentStatus(Enum):
    Pending = "Pending"
    Paid = "Paid"
    Failed = "Failed"
    Processing = "Processing"
    Refunded = "Refunded"


class LenderPayments(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "lender_payments"

    payment_percentage = Column(Integer, nullable=False)
    payment_amount = Column(Numeric, nullable=False)
    payment_status = Column(SQLAEnum(PaymentStatus))

    # Foreign Keys
    article_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False
    )
    transaction_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False
    )
