from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class Categories(Base):
    __tablename__ = "categories"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    is_default = Column(Boolean)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    materials = relationship("Materials", backref="categories")
    product_categories = relationship("ProductCategories", backref="categories")
    categories_for_user = relationship("CategoriesForUser", backref="categories")
    types = relationship("Types", backref="categories")
    pricing_tiers = relationship("PricingTier", backref="categories")
