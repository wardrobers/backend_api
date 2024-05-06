from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class Sizing(Base):
    __tablename__ = "sizing"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    label = Column(String, nullable=False)
    measurements = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    variant_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("variants.uuid"), nullable=False
    )
    size_system_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("size_systems.uuid"), nullable=False
    )