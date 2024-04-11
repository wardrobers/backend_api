from uuid import uuid4
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base


class VariantColor(Base):
    __tablename__ = "variant_colors"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    color = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    variants = relationship("Variant", back_populates="color")
