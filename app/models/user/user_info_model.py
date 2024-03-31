from uuid import uuid4
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from .user_model import User


Base = declarative_base()


class UserInfo(Base):
    __tablename__ = "user_info"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    users_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="user_info")
