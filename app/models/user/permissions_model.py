from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class Permissions(Base):
    __tablename__ = "permissions"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    crud = Column(String(6), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    role_permissions = relationship("RolePermissions", back_populates="permissions")
