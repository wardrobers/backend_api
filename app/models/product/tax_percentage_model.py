from uuid import uuid4
from sqlalchemy import Column, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from ..basemixin import Base


class TaxPercentage(Base):
    __tablename__ = "tax_percentage"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    percentage = Column(Numeric, nullable=False)
    created_at = Column(DateTime, server_default="now()")
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
