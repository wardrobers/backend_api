from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class SizeSystems(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "size_systems"

    name = Column(String, nullable=False)
    description = Column(Text)

    # Relationships
    sizings = relationship("Sizing", back_populates="size_system")
