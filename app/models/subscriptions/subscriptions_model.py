from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.base_model import Base


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    subscription_start = Column(DateTime, nullable=True)
    subscription_finish = Column(DateTime, nullable=True)
    count_free_orders = Column(Integer, nullable=True)
    count_orders_available_by_subscription = Column(Integer, nullable=True)
    count_orders_closed_by_subscription = Column(Integer, nullable=True)
    purchase_url = Column(String, nullable=True)

    # Foreign Keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    subscription_type_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("subscription_types.id"), nullable=False
    )
