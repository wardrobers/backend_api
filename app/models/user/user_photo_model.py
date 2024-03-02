from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()


class UserPhoto(Base):
    __tablename__ = "users_photos"
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"))
    storage_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime)

    user = relationship("User", back_populates="users_photos")