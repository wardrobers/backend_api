from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.base_model import Base


class RoleType(str, Enum):
    """
    Enum representing user roles in a clothing rental platform.
    """

    Admin = "Admin"  # Full system administration rights
    Lender = "Lender"  # Can list items, manage inventory, set prices, handle rentals
    Renter = "Renter"  # Can browse items, rent items, manage their profile
    Moderator = "Moderator"  # Can moderate content, reviews, and user interactions
    Guest = "Guest"  # Unregistered user, limited browsing access


class Roles(Base):
    __tablename__ = "roles"

    code = Column(String, nullable=False)
    name = Column(SQLAEnum(RoleType))

    # Relationships
    role = relationship(
        "UserRoles",
        backref="roles",
        cascade="all, delete-orphan",
    )
    role_permissions = relationship(
        "RolePermissions",
        backref="roles",
        cascade="all, delete-orphan",
    )
