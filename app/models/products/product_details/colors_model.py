from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class Colors(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "colors"

    name = Column(String)

    # Relationships
    variant = relationship(
        "app.models.products.core.variants_model.Variants", backref="colors"
    )
