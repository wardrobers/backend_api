from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class AccessoriesSize(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "accessories_size"

    name = Column(String)

    # Relationships
    product = relationship("Products", backref="accessories_size")
