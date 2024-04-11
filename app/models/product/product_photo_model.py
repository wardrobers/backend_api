from sqlalchemy import Column, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class ProductPhoto(Base):
    __tablename__ = "product_photos"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    index = Column(Integer, default=1)
    showcase = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    product_uuid = Column(UUID(as_uuid=True), ForeignKey("products.uuid"))
