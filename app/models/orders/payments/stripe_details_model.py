from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class StripeDetails(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "stripe_details"

    stripe_charge_id = Column(BYTEA, nullable=True, default=None)
    stripe_customer_id = Column(String, nullable=True, default=None)
    stripe_payment_intent_id = Column(String, nullable=True, default=None)
    stripe_error_log = Column(
        Text,
        nullable=True,
        default=None,
    )

    # Foreign Keys
    transaction_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id"),
        nullable=False,
    )

    def __repr__(self):
        return f"<StripeDetails(uuid={self.id}, transaction_id={self.transaction_id})>"
