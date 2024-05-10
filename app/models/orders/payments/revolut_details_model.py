from sqlalchemy import Column, ForeignKey, Strings
from sqlalchemy.dialects.postgresql import UUID

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class RevolutDetails(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "revolut_details"

    revolut_account_id = Column(String, nullable=True)

    # Foreign keys
    transaction_id = Column(
        UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False
    )

    def __repr__(self):
        return f"<RevolutDetails(uuid={self.id}, transaction_id={self.transaction_id})>"
