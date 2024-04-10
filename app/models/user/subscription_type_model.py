from sqlalchemy import Column, DateTime, Integer, Numeric, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


from ..basemixin import Base


class SubscriptionType(Base):
    __tablename__ = "subscription_types"
    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    name = Column(
        String, nullable=True
    )  # Note: Nullable=True as per the table definition
    period_uuid = Column(UUID(as_uuid=True), ForeignKey("subscription_periods.uuid"), nullable=False)
    price = Column(Numeric, nullable=False)
    count_free_orders = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    # Assuming Subscription model exists and is correctly defined
    subscription = relationship("Subscription", back_populates="subscription_type")
