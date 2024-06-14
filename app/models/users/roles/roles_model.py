from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Roles(Base):
    __tablename__ = "roles"

    code = Column(String, nullable=False)
    name = Column(String)

    # Relationships
    users = relationship(
        "UserRoles",
        backref="roles",
    )
    role_permissions = relationship(
        "RolePermissions",
        backref="roles",
    )
