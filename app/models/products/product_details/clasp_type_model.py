from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class ClaspType(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "clasp_types"

    name = Column(String, nullable=True)

    # Relationships
    product = relationship("Products", backref="clasp_types")
