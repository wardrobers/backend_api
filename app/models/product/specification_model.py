from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class Specification(Base):
    __tablename__ = "specifications"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    index = Column(Integer)
    value = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    article_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('article.uuid'), nullable=False)

    # Relationships
    article = relationship("Article", back_populates="specification")