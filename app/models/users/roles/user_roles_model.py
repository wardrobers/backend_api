from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from app.models.base_model import Base


class UserRoles(Base):
    __tablename__ = "user_roles"

    # Foreign keys
    user_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
    )
    role_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id"),
        primary_key=True,
    )

    # Relationships
    user = relationship("app.models.users.core.users_model.Users", backref="user_roles")
    roles = relationship(
        "app.models.users.roles.roles_model.Roles", backref="user_roles"
    )
