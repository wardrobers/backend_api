from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


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
    roles = relationship(
        "app.models.users.roles.roles_model.Roles", back_populates="role_permissions"
    )
    permissions = relationship(
        "app.models.users.roles.permissions_model.Permissions",
        back_populates="role_permissions",
    )
