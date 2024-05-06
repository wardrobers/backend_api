from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class UserPhotos(Base):
    __tablename__ = "user_photos"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime)

    # Foreign Keys
    user_uuid = mapped_column(UUID(as_uuid=True), ForeignKey("users.uuid"))
