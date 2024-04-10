from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Foreign keys
    user_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), primary_key=True
    )
    role_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.uuid"), primary_key=True
    )
