from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class UserBasket(Base):
    __tablename__ = "user_basket"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    count = Column(Integer, default=1)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    user_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    stock_keeping_unit_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_keeping_unit.id"), nullable=False
    )
