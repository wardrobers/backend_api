from sqlalchemy import Column, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models import Base


class RepairLogs(Base):
    __tablename__ = "repair_logs"

    description = Column(Text, nullable=True)
    cost = Column(Numeric, nullable=True)
    repair_date = Column(DateTime, nullable=False)

    # Foreign Keys
    article_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("articles.id"),
        nullable=False,
    )
