from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class SubscriptionType(Base):
    __tablename__ = "subscription_types"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=True)
    price = Column(Numeric, nullable=False)
    count_free_orders = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Foreign Keys
    period_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("subscription_periods.uuid"), nullable=False
    )

    # Relationships
    subscription = relationship("Subscription", back_populates="subscription_type")
