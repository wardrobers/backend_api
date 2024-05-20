from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from app.models.common import Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin


class OccasionalCategories(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "occasional_categories"

    name = Column(String, nullable=False)
    img_url = Column(String, nullable=False)

    # Relationships
    product_occasional_categories = relationship(
        "ProductOccasionalCategories", backref="occasional_categories"
    )
    promotions_occasional_categories = relationship(
        "PromotionsOccasionalCategories", backref="occasional_categories"
    )


class ProductOccasionalCategories(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "product_occasional_categories"

    # Foreign Keys
    product_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    occasional_category_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("occasional_categories.id"), nullable=False
    )