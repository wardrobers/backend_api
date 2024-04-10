from uuid import uuid4
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func

from ..basemixin import Base


class Permission(Base):
    __tablename__ = "permissions"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    crud = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    role_permission = relationship("RolePermission", back_populates="permission")
