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
    product = relationship("Products", secondary="product_types", backref="types")
    product_types = relationship("ProductTypes", backref="types")


class ProductTypes(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "product_types"

    # Foreign Keys
    product_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False, comment="Товар"
    )
    type_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("types.id"), nullable=False, comment="Тип вещи"
    )
