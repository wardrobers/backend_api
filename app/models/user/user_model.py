from uuid import uuid4
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    uuid = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    login = Column(String, nullable=False)
    super_admin = Column(Boolean)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, nullable=False, default=False)
    last_login_at = Column(DateTime)
    marketing_consent = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default="now()", nullable=False)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user_info = relationship("UserInfo", back_populates="user", uselist=False) 
    user_activity = relationship("UserActivity", back_populates="user", uselist=False)
    user_subscription = relationship(
        "Subscription", back_populates="user", uselist=False
    )
    users_photos = relationship("UsersPhotos", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")
