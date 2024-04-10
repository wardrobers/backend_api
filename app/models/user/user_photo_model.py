from uuid import uuid4
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base


class UsersPhotos(Base):
    __tablename__ = "users_photos"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    storage_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    user_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("users.uuid"))

    # Relationships
    user = relationship("User", back_populates="user_photos")
