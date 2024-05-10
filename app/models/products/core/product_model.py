from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class Product(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "products"

    sku_product = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    instructions = Column(String)

    # Foreign Keys
    sku_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_keeping_unit.id"), nullable=False
    )
    brand_id = mapped_column(UUID(as_uuid=True), ForeignKey("brands.id"))
    clothing_size_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("clothing_sizes.id")
    )
    clasp_type_id = mapped_column(UUID(as_uuid=True), ForeignKey("clasp_types.id"))
    product_fit_id = mapped_column(UUID(as_uuid=True), ForeignKey("product_fit.id"))
    status_code = mapped_column(String, ForeignKey("product_status.code"))

    # Relationships
    types = relationship("ProductTypes", backref="products")
    photos = relationship("ProductPhotos", backref="products")
    variants = relationship("Variants", backref="products")
    user_reviews_and_ratings = relationship("UserReviewsAndRatings", backref="products")
    categories = relationship("ProductCategories", backref="products")
    promotions_products = relationship("PromotionsProducts", backref="products")
    pricing_tiers = relationship("PricingTier", backref="products")
    accessory_size = relationship("AccessoriesSize", backref="products")

    def __repr__(self):
        return f"<Product(uuid={self.id}, name='{self.name}', sku_product='{self.sku_product}')>"
