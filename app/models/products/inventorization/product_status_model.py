from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


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
    product = relationship(
        "app.models.products.core.products_model.Products", backref="product_status"
    )
