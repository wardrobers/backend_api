from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class StripeDetails(Base):
    __tablename__ = "stripe_details"

    uuid = mapped_column(
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
    transaction_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transactions.uuid"),
        nullable=False,
        comment="Транзакция",
    )

    # Relationships
    transaction = relationship("Transaction", backref="stripe_details")

    def __repr__(self):
        return f"<StripeDetails(uuid={self.uuid}, transaction_uuid={self.transaction_uuid})>"