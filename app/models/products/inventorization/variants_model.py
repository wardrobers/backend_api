from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
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
