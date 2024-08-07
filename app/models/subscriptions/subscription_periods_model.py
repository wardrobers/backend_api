from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class SubscriptionPeriods(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "subscription_periods"

    name = Column(String, nullable=True)

    # Relationships
    subscription_types = relationship(
        "SubscriptionTypes", backref="subscription_periods"
    )
