from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


from ..basemixin import Base


class Subscription(Base):
    __tablename__ = "subscriptions"
    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    user_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("users.uuid"))
    subscription_type_uuid = mapped_column(
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

    user = relationship("User", back_populates="user_subscription")
    subscription_type = relationship("SubscriptionType", back_populates="subscriptions", uselist=False)
