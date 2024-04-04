from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from ..basemixin import Base


class UserPhoto(Base):
    __tablename__ = "users_photos"
    uuid = Column(UUID(as_uuid=True), server_default=func.uuid_generate_v4())
    user_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("users.uuid"))
    storage_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime)
    user = relationship("User", back_populates="user_photos")
