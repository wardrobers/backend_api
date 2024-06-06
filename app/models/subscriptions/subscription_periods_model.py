from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.repositories.common import Base, BaseMixin


class SubscriptionPeriods(Base, BaseMixin):
    __tablename__ = "subscription_periods"

    name = Column(String, nullable=True)

    # Relationships
    subscription_types = relationship(
        "SubscriptionTypes", backref="subscription_periods"
    )
