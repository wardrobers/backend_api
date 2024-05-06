from uuid import uuid4
from sqlalchemy import Column, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from ...common.base_model import Base


class RolePermissions(Base):
    __tablename__ = "role_permissions"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    to_create = Column(Boolean, default=False, name="create")
    to_read = Column(Boolean, default=False, name="read")
    to_update = Column(Boolean, default=False, name="update")
    to_delete = Column(Boolean, default=False, name="delete")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    role_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.uuid"), nullable=False
    )
    permission_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("permissions.uuid"), nullable=False
    )

    # Relationships
    roles = relationship("Roles", back_populates="role_permissions")
    permissions = relationship("Permissions", back_populates="role_permissions")
