from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models import Base


class TransactionStatus(Enum):
    Succeeded = "Succeeded"
    Pending = "Pending"
    Failed = "Failed"
    Refunded = "Refunded"
    Chargeback = "Chargeback"


class Transactions(Base):
    __tablename__ = "transactions"

    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    transaction_date = Column(DateTime)
    status = Column(SQLAEnum(TransactionStatus))

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    payment_method_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("payment_methods.id"), nullable=False
    )
    order_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    user_address_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("user_addresses.id"), nullable=False
    )

    # Relationships
    revolut_details = relationship(
        "app.models.orders.payments.revolut_details_model.RevolutDetails",
        backref="transactions",
    )
    stripe_details = relationship(
        "app.models.orders.payments.stripe_details_model.StripeDetails",
        backref="transactions",
    )
    lender_payment = relationship(
        "app.models.orders.paymentslender_payments_model.LenderPayments",
        backref="transactions",
    )

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, currency='{self.currency}', status='{self.status}')>"
