from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models import Base


class SubscriptionPeriods(Base):
    __tablename__ = "subscription_periods"

    name = Column(String, nullable=True)

    # Relationships
    subscription_types = relationship(
        "SubscriptionTypes", backref="subscription_periods"
    )
