from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class ProductFit(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "product_fit"

    type = Column(String, nullable=False)

    # Relationships
    product = relationship("Products", backref="product_fit")
