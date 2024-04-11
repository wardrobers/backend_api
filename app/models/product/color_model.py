from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class Color(Base):
    __tablename__ = "colors"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    color = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    product = relationship("Product", back_populates="color")
