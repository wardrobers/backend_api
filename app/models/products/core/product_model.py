from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class Product(Base):
    __tablename__ = "products"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sku_product = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    instructions = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    sku_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_keeping_unit.uuid"), nullable=False
    )
    brand_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("brands.uuid"))
    clothing_size_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("clothing_sizes.uuid")
    )
    clasp_type_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("clasp_types.uuid"))
    product_fit_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("product_fit.uuid"))
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
        return f"<Product(uuid={self.uuid}, name='{self.name}', sku_product='{self.sku_product}')>"
