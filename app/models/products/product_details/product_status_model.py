from enum import Enum
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum
from uuid import uuid4

from ...common.base_model import Base


class ProductStatus(Enum):
    InUse = "InUse"
    Available = "Available"
    NotAvailable = "NotAvailable"
    ComingSoon = "ComingSoon"
    Discontinued = "Discontinued"


class ProductStatus(Base):
    __tablename__ = "product_status"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String, nullable=False)
    name = Column(SQLAEnum(ProductStatus), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    product = relationship("Product", backref="product_status")
