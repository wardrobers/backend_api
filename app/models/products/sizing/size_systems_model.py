from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class SizeSystems(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "size_systems"

    name = Column(String, nullable=False)
    description = Column(Text)

    # Relationships
    sizings = relationship(
        "app.models.products.sizing.sizing_model.Sizing", back_populates="size_system"
    )
