from sqlalchemy import Column, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column


from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class UserActivity(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "user_activity"

    total_confirmed_orders = Column(Integer, nullable=False, default=0)
    total_canceled_orders = Column(Integer, nullable=False, default=0)
    activity_orders = Column(Integer, nullable=False, default=0)
    subscription_now = Column(Boolean, nullable=False, default=False)
    total_money_spent = Column(Numeric, nullable=True)

    # Foreign Keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
