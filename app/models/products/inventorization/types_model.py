from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


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
