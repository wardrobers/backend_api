from pydantic import UUID4
from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import  relationship, mapped_column
from sqlalchemy.sql import func
from ..basemixin import Base


class Role(Base):
    __tablename__ = 'roles'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, server_default="now()")
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user = relationship('User', secondary='user_roles', back_populates='roles')


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String, nullable=False)
    # super_admin = Column(Boolean)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, nullable=False, default=False)
    last_login_at = Column(DateTime)
    marketing_consent = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default="now()", nullable=False)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user_info = relationship("UserInfo", back_populates="user", uselist=False)
    # user_activity = relationship("UserActivity", back_populates="user", uselist=False)
    users_photos = relationship("UsersPhotos", back_populates="user")
    roles = relationship('Role', secondary='user_roles', back_populates='user')
    orders = relationship('Order', back_populates='user')

class UserRole(Base):
    __tablename__ = 'user_roles'
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), primary_key=True)
    role_uuid = Column(UUID(as_uuid=True), ForeignKey('roles.uuid'), primary_key=True)
    created_at = Column(DateTime, server_default="now()")
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime) 