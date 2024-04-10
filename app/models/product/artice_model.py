from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class Article(Base):
    __tablename__ = "article"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    article = Column(UUID(as_uuid=True), unique=True)
    factory_number = Column(String)
    size = Column(String)
    color = Column(String)
    times_used = Column(Integer, nullable=False, default=0)
    hours_used = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    stock_keeping_unit_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_keeping_unit.uuid"), nullable=False
    )
    status_code = mapped_column(
        UUID(as_uuid=True), ForeignKey("article_statuses.status_code"), nullable=False
    )
    types_of_operation_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("types_of_operations.uuid"), nullable=False
    )

    # Relationships
    stock_keeping_unit = relationship("StockKeepingUnit", back_populates="article")
    article_status = relationship("ArticleStatus", back_populates="article")
    types_of_operations = relationship("TypesOfOperations", back_populates="article")
    specification = relationship("Specification", back_populates="article")
    order_item = relationship("Specification", back_populates="article")
