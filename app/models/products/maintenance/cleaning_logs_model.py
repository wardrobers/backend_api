from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models import Base


class CleaningLogs(Base):
    __tablename__ = "cleaning_logs"

    article = Column(String, nullable=False)
    description = Column(Text)
    cost = Column(Numeric)
    cleaning_date = Column(DateTime, nullable=False)

    # Foreign keys
    article_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False
    )
