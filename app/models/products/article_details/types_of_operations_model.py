from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class TypesOfOperations(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "types_of_operations"

    name = Column(String, nullable=True, default=None)

    # Relationships
    articles = relationship("Article", backref="types_of_operations")
