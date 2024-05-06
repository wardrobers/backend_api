from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base

class PromotionsProducts(Base):
    __tablename__ = 'promotions_products'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    product_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('products.uuid'), nullable=False)
    promotion_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('promotions_and_discounts.uuid'), nullable=False)