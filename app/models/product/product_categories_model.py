from sqlalchemy import Column, DateTime, String, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pydantic import UUID4
import datetime
from sqlalchemy.orm import declarative_base

# Ensure you are importing Product and Category models in this file
# This ensures the relationships are properly constructed
# from .product_model import Product  # noqa: F401
# from .category_model import Category  # noqa: F401

from ..basemixin import Base


class ProductCategory(Base):
    __tablename__ = "product_categories"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=UUID4)
    product_uuid = Column(UUID(as_uuid=True), ForeignKey("products.uuid"))
    category_uuid = Column(UUID(as_uuid=True), ForeignKey("categories.uuid"))
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    deleted_at = Column(DateTime)
