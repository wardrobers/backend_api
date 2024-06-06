from enum import Enum

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models import Base


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

    type = Column(SQLAEnum(PaymentMethodType))
    provider = Column(SQLAEnum(PaymentProvider))
    card_hash = Column(BYTEA)
    token = Column(String)
    exp_month = Column(Integer)
    exp_year = Column(Integer)
    lender = Column(Boolean, default=False)

    # Relationships
    transactions = relationship(
        "app.model.orders.payments.transactions_model.Transactions",
        backref="payment_methods",
    )
