from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class Variants(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "variants"

    name = Column(String, nullable=False)
    index = Column(Integer)

    # Foreign Keys
    product_id = mapped_column(UUID(as_uuid=True), ForeignKey("products.id"))
    sku_id = mapped_column(UUID(as_uuid=True), ForeignKey("stock_keeping_units.id"))
    color_id = mapped_column(UUID(as_uuid=True), ForeignKey("colors.id"))

    # Relationships
    sizing = relationship("Sizing", backref="variants")
    promotions = relationship(
        "PromotionsAndDiscounts", secondary="promotions_variants", backref="variants"
    )
