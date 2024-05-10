from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class StockKeepingUnit(Base):
    __tablename__ = "stock_keeping_unit"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sku_product = Column(String, nullable=False)
    sku_article = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    articles = relationship("Article", backref="stock_keeping_unit")
    variants = relationship("Variants", backref="stock_keeping_unit")
    user_basket = relationship("UserBasket", backref="stock_keeping_unit")
