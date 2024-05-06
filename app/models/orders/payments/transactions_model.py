from enum import Enum
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum
from uuid import uuid4

from ...common.base_model import Base


class TransactionStatus(Enum):
    Succeeded = "Succeeded"
    Pending = "Pending"
    Failed = "Failed"
    Refunded = "Refunded"
    Chargeback = "Chargeback"


class Transactions(Base):
    __tablename__ = "transactions"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    transaction_date = Column(DateTime)
    status = Column(SQLAEnum(TransactionStatus))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    user_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    payment_method_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("payment_methods.uuid"), nullable=False
    )
    order_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.uuid"), nullable=False
    )
    user_address_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_addresses.uuid"), nullable=False
    )

    # Relationships
    revolut_details = relationship("RevolutDetails", backref="transactions")
    stripe_details = relationship("StripeDetails", backref="transactions")
    lender_payment = relationship("LenderPayments", backref="transactions")

    def __repr__(self):
        return f"<Transaction(uuid={self.uuid}, amount={self.amount}, currency='{self.currency}', status='{self.status}')>"