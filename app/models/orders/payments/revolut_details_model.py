from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from app.repositories.common import Base, BaseMixin


class RevolutDetails(Base, BaseMixin):
    __tablename__ = "revolut_details"

    revolut_account_id = Column(String, nullable=True)

    # Foreign keys
    transaction_id = Column(
        UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False
    )

    def __repr__(self):
        return f"<RevolutDetails(id={self.id}, transaction_id={self.transaction_id})>"
