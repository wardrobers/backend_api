from sqlalchemy import Column, ForeignKey, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4


from ..basemixin import Base


class Order(Base):
    __tablename__ = "orders"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    status_code = Column(UUID(as_uuid=True), unique=True)
    total_price = Column(Numeric)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    user_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("users.uuid"))

    # Relationships
    user = relationship("User", back_populates="order")
