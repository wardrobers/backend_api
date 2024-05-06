from sqlalchemy import Column, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class ClothingSizes(Base):
    __tablename__ = "clothing_sizes"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    back_length = Column(Numeric, nullable=True)
    sleeve_length = Column(Numeric, nullable=True)
    pants_length = Column(Numeric, nullable=True)
    skirt_length = Column(Numeric, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
