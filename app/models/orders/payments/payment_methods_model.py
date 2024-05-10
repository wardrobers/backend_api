from enum import Enum
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum
from uuid import uuid4

from ...common.base_model import Base


class PaymentMethodType(Enum):
    CreditCard = "CreditCard"
    DebitCard = "DebitCard"
    BankTransfer = "BankTransfer"
    GiftCard = "GiftCard"
    PostPayment = "PostPayment"
    Wallet = "Wallet"


class PaymentProvider(Enum):
    Stripe = "Stripe"
    PayPal = "PayPal"
    Revolut = "Revolut"
    ApplePay = "ApplePay"
    GooglePay = "GooglePay"
    Klarna = "Klarna"


class PaymentMethods(Base):
    __tablename__ = "payment_methods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(SQLAEnum(PaymentMethodType))
    provider = Column(SQLAEnum(PaymentProvider))
    card_hash = Column(BYTEA)
    token = Column(String)
    exp_month = Column(Integer)
    exp_year = Column(Integer)
    lender = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    transactions = relationship("Transactions", backref="payment_methods")
