from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class ProductFit(Base):
    __tablename__ = "product_fit"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    product = relationship("Product", backref="product_fit")