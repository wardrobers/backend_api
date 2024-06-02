from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class SubscriptionTypes(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "subscription_types"

    name = Column(String, nullable=True)
    price = Column(Numeric, nullable=False)
    count_free_orders = Column(Integer, nullable=False)

    # Foreign Keys
    period_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subscription_periods.id"),
        nullable=False,
    )

    # Relationships
    subscriptions = relationship("Subscriptions", backref="subscription_types")
