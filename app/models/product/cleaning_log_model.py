from sqlalchemy import Column, DateTime, Numeric, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class CleaningLog(Base):
    __tablename__ = 'cleaning_logs'

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    article = Column(String, nullable=False)
    description = Column(Text)
    cost = Column(Numeric)
    cleaning_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    # Foreign keys
    article_uuid = mapped_column(UUID(as_uuid=True), ForeignKey('article.uuid'), nullable=False)
    
    # Relationships
    article = relationship("Article", back_populates="cleaning_logs")