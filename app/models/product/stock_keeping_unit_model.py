from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class StockKeepingUnit(Base):
    __tablename__ = "stock_keeping_unit"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    sku_name = Column(String, nullable=False)
    sku_code = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    article = relationship("Article", back_populates="stock_keeping_unit")
    user_basket = relationship("UserBasket", back_populates="sku")
    variants = relationship("Variant", back_populates="sku")
