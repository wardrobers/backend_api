from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class Subscriptions(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
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
