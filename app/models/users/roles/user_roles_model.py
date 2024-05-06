from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func

from ...common.base_model import Base


class UserRoles(Base):
    __tablename__ = "user_roles"

    created_at = Column(DateTime, nullable=False, default=func.now(), comment="Создано")
    updated_at = Column(
        DateTime, nullable=True, onupdate=func.now(), comment="Отредактировано"
    )
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Foreign keys
    user_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid"),
        primary_key=True,
        comment="Пользователь",
    )
    role_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.uuid"),
        primary_key=True,
        comment="Индетифекатор",
    )

    # Relationships
    user = relationship("User", backref="user_roles")
    roles = relationship("Roles", backref="user_roles")
