from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class CRUDOperation(Enum):
    Create = "Create"
    Read = "Read"
    Update = "Update"
    Delete = "Delete"


class Permissions(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "permissions"

    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    crud = Column(SQLAEnum(CRUDOperation), nullable=False)

    # Relationships
    role_permissions = relationship("RolePermissions", backref="permissions")
