from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


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
