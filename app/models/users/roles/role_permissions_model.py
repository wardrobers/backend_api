from sqlalchemy import Column, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class RolePermissions(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "role_permissions"

    to_create = Column(Boolean, default=False, name="create")
    to_read = Column(Boolean, default=False, name="read")
    to_update = Column(Boolean, default=False, name="update")
    to_delete = Column(Boolean, default=False, name="delete")

    # Foreign keys
    role_id = mapped_column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    permission_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("permissions.id"), nullable=False
    )

    # Relationships
    roles = relationship("Roles", back_populates="role_permissions")
    permissions = relationship("Permissions", back_populates="role_permissions")
