from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class Roles(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "roles"

    code = Column(String, nullable=False)
    name = Column(String)

    # Relationships
    users = relationship(
        "app.models.users.core.users_model.Users",
        secondary="user_roles",
        backref="roles",
    )
