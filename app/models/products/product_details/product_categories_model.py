from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class ProductCategories(Base):
    __tablename__ = "product_categories"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    product_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("products.uuid"))
    category_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("categories.uuid"))