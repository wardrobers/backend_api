from enum import Enum
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAEnum
from uuid import uuid4

from ...common.base_model import Base


class CRUDOperation(Enum):
    Create = "Create"
    Read = "Read"
    Update = "Update"
    Delete = "Delete"


class Permissions(Base):
    __tablename__ = "permissions"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    crud = Column(SQLAEnum(CRUDOperation), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    role_permissions = relationship("RolePermissions", backref="permissions")
