from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models import Base


class ProductCurrentStatus(Enum):
    InUse = "InUse"
    Available = "Available"
    NotAvailable = "NotAvailable"
    ComingSoon = "ComingSoon"
    Discontinued = "Discontinued"


class ProductStatus(Base):
    __tablename__ = "product_status"

    code = Column(String, nullable=False)
    name = Column(SQLAEnum(ProductCurrentStatus), nullable=False)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="product_status"
    )
