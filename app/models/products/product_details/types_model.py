from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class Types(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "types"

    name = Column(String, nullable=False)

    # Foreign keys
    category_id = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id"))

    # Relationships
    product = relationship("Product", secondary="product_types", backref="types")
    product_types = relationship("ProductTypes", backref="types")
