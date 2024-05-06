from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class ProductStatus(Base):
    __tablename__ = "product_status"
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String, nullable=False)
    name = Column(String(12), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)
