from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    subscription_start = Column(DateTime)
    subscription_finish = Column(DateTime)
    count_free_orders = Column(Integer)
    count_orders_available_by_subscription = Column(Integer)
    count_orders_closed_by_subscription = Column(Integer)
    purchase_url = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Foreign Keys
    user_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    subscription_type_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("subscription_types.uuid"), nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="subscription")
    subscription_type = relationship("SubscriptionType", back_populates="subscription")
