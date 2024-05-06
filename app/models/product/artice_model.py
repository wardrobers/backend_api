from sqlalchemy import Column, DateTime, Integer, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class Article(Base):
    __tablename__ = "article"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    article = Column(String, nullable=False)
    sku_article = Column(String, nullable=False)
    owner_type = Column(String(8), nullable=False)
    factory_number = Column(String)
    times_used = Column(Integer, default=0, nullable=False)
    hours_used = Column(Integer, default=0, nullable=False)
    min_rental_days = Column(Integer, nullable=False, default=2)
    buffer_days = Column(Integer, nullable=False, default=1)
    pre_rental_buffer = Column(Integer, nullable=True, default=0)
    for_cleaning = Column(Boolean, nullable=True, default=False)
    for_repair = Column(Boolean, nullable=True, default=False)
    condition = Column(String(9), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    stock_keeping_unit_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_keeping_unit.uuid"), nullable=False
    )
    status_code = mapped_column(
        String, ForeignKey("article_statuses.status_code"), nullable=False
    )
    types_of_operation_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("types_of_operations.uuid"), nullable=False
    )

    # Relationships
    sku = relationship("StockKeepingUnit", back_populates="article")
    article_status = relationship("ArticleStatus", back_populates="article")
    types_of_operations = relationship("TypesOfOperations", back_populates="article")
    order_item = relationship("Specification", back_populates="article")
