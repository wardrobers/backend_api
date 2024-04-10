from uuid import uuid4
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Foreign Keys
    user_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="user_info")
