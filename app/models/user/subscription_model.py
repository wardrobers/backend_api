from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Subscription(Base):
    __tablename__ = "subscriptions"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"))
    subscription_type_uuid = Column(
        UUID(as_uuid=True), ForeignKey("subscription_types.uuid")
    )
    subscription_start = Column(DateTime)
    subscription_finish = Column(DateTime)
    count_free_orders = Column(Integer)
    count_orders_available_by_subscription = Column(Integer)
    count_orders_closed_by_subscription = Column(Integer)
    purchase_url = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", back_populates="subscriptions")
    subscription_type = relationship("SubscriptionType", back_populates="subscriptions")