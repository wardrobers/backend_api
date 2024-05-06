from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class Roles(Base):
    __tablename__ = "roles"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    users = relationship("User", secondary="user_roles", backref="roles")
