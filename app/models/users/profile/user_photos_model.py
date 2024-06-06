from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.base_model import Base


class UserPhotos(Base):
    __tablename__ = "user_photos"

    image_url = Column(String, nullable=False)

    # Foreign Keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
