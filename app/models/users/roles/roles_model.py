from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.repositories.common import Base, BaseMixin


class Roles(Base, BaseMixin):
    __tablename__ = "roles"

    code = Column(String, nullable=False)
    name = Column(String)

    # Relationships
    users = relationship(
        "app.models.users.core.users_model.Users",
        secondary="user_roles",
        backref="roles",
    )
