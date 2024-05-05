from uuid import uuid4
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from ..basemixin import Base


class Roles(Base):
    __tablename__ = "roles"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, server_default="now()")
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    # Relationships
    user = relationship("User", secondary="user_roles", back_populates="role")
    role_permission = relationship("RolePermission", back_populates="role")
