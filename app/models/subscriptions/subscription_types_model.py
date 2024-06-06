from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.repositories.common import Base, BaseMixin


class SubscriptionTypes(Base, BaseMixin):
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
