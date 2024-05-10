from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class RevolutDetails(Base):
    __tablename__ = "revolut_details"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    revolut_account_id = Column(
        String, nullable=True, comment="Revolut account identifier"
    )
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")
    deleted_at = Column(DateTime, comment="Удалено")

    # Foreign keys
    transaction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("transactions.id"),
        nullable=False,
        comment="Транзакция",
    )

    def __repr__(self):
        return f"<RevolutDetails(uuid={self.id}, transaction_id={self.transaction_id})>"
