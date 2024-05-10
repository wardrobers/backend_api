from sqlalchemy import Column, Integer, ForeignKey, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


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
