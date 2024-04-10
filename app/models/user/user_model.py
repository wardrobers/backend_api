from uuid import uuid4
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base

from .user_activity_model import UserActivity
from .user_photo_model import UsersPhotos
from .role_model import Role


class User(Base):
    __tablename__ = "users"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, default=False)
    last_login_at = Column(DateTime)
    marketing_consent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    order = relationship("Order", back_populates="user")
    subscription = relationship("Subscription", back_populates="user")
    user_info = relationship("UserInfo", uselist=False, back_populates="user")
    user_activity = relationship("UserActivity", uselist=False, back_populates="user")
    user_basket = relationship("UserBasket", uselist=False, back_populates="user")
    user_photos = relationship("UsersPhotos", back_populates="user")
    role = relationship("Role", secondary="user_roles", back_populates="user")
    category_for_user = relationship("CategoriesForUser", back_populates="user")
