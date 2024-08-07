from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class Roles(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "roles"

    code = Column(String, nullable=False)
    name = Column(String)

    # Relationships
    users = relationship("User", secondary="user_roles", backref="roles")
