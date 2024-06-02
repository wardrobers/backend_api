from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class ProductCurrentStatus(Enum):
    InUse = "InUse"
    Available = "Available"
    NotAvailable = "NotAvailable"
    ComingSoon = "ComingSoon"
    Discontinued = "Discontinued"


class ProductStatus(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "product_status"

    code = Column(String, nullable=False)
    name = Column(SQLAEnum(ProductCurrentStatus), nullable=False)

    # Relationships
    product = relationship("Products", backref="product_status")
