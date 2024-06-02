from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class UserActivity(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "user_activity"

    total_confirmed_orders = Column(Integer, nullable=False, default=0)
    total_canceled_orders = Column(Integer, nullable=False, default=0)
    activity_orders = Column(Integer, nullable=False, default=0)
    subscription_now = Column(Boolean, nullable=False, default=False)
    total_money_spent = Column(Numeric, nullable=True)

    # Foreign Keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
