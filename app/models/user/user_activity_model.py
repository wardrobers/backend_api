from sqlalchemy import Column, DateTime, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()


class UserActivity(Base):
    __tablename__ = "user_activity"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    total_confirmed_orders = Column(Integer, default=0, nullable=False)
    total_canceled_orders = Column(Integer, default=0, nullable=False)
    activity_orders = Column(Integer, default=0, nullable=False)
    subscription_now = Column(Boolean, default=False, nullable=False)
    total_money_spent = Column(Numeric, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)
