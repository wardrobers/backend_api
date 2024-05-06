from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    amount = Column(Numeric, nullable=False)
    currency = Column(String, nullable=False)
    transaction_date = Column(DateTime)
    status = Column(String(10))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False)
    payment_method_uuid = Column(UUID(as_uuid=True), ForeignKey('payment_methods.uuid'), nullable=False)
    order_uuid = Column(UUID(as_uuid=True), ForeignKey('orders.uuid'), nullable=False)
    user_address_uuid = Column(UUID(as_uuid=True), ForeignKey('user_addresses.uuid'), nullable=False)

    # Relationships
    user = relationship("User", backref="transactions")
    payment_method = relationship("PaymentMethod", backref="transactions")
    order = relationship("Order", backref="transactions")
    user_address = relationship("UserAddress", backref="transactions")

    def __repr__(self):
        return f"<Transaction(uuid={self.uuid}, amount={self.amount}, currency='{self.currency}', status='{self.status}')>"
