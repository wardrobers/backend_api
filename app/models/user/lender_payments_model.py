from sqlalchemy import Column, DateTime, String, ForeignKey, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship, backref
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class LenderPayments(Base):
    __tablename__ = "lender_payments"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    payment_percentage = Column(Integer, nullable=False)
    payment_amount = Column(Numeric, nullable=False)
    payment_status = Column(String(10))
    updated_at = Column(DateTime, onupdate=func.now())
    created_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    article_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('article.uuid'), nullable=False)

    # Relationships
    article = relationship("Article", backref=backref("lender_payments", uselist=True))