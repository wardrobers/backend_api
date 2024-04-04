from uuid import uuid4
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from ..basemixin import Base


class Roler(Base):
    __tablename__ = 'roles'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

class UserrInfo(Base):
    __tablename__ = 'user_info'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    name = Column(String, nullable=False)
    last_name = Column(String)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

class UserrRole(Base):
    __tablename__ = 'user_roles'
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), primary_key=True)
    role_uuid = Column(UUID(as_uuid=True), ForeignKey('roles.uuid'), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user = relationship('Userr', back_populates='photos')

class Userr(Base):
    __tablename__ = 'users'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_notificated = Column(Boolean, default=False)
    last_login_at = Column(DateTime)
    marketing_consent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    info = relationship('UserrInfo', back_populates='user', uselist=False)
    roles = relationship('UserrRole', secondary='user_roles', back_populates='user')
    photos = relationship('UserrPhoto', back_populates='user')

class UserrPhoto(Base):
    __tablename__ = 'users_photoes'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    storage_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime)
    user = relationship('Userr', back_populates='photos')


Roler.user = relationship('Userr', secondary='user_roles', back_populates='roles')