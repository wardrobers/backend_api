from uuid import uuid4
from sqlalchemy import Column, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base


class RolePermissions(Base):
    __tablename__ = "role_permissions"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    create = Column(Boolean, default=False)
    read = Column(Boolean, default=False)
    update = Column(Boolean, default=False)
    delete = Column(Boolean, default=False)
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
    role = relationship("Role", back_populates="role_permission")
    permission = relationship("Permission", back_populates="role_permission")
