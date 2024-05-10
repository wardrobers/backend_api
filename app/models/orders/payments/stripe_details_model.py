from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class StripeDetails(Base):
    __tablename__ = "stripe_details"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    stripe_charge_id = Column(
        BYTEA, nullable=True, default=None, comment="Encrypted Stripe charge ID"
    )
    stripe_customer_id = Column(String, nullable=True, default=None)
    stripe_payment_intent_id = Column(String, nullable=True, default=None)
    stripe_error_log = Column(
        Text,
        nullable=True,
        default=None,
        comment="Store error details for failed transactions",
    )
    created_at = Column(DateTime, nullable=True, default=func.now(), comment="Создано")
    updated_at = Column(
        DateTime, nullable=True, onupdate=func.now(), comment="Отредактировано"
    )
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Foreign Keys
    transaction_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id"),
        nullable=False,
        comment="Транзакция",
    )

    def __repr__(self):
        return f"<StripeDetails(uuid={self.id}, transaction_id={self.transaction_id})>"
