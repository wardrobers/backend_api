from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class ClaspType(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "clasp_types"

    name = Column(String, nullable=True)

    # Relationships
    product = relationship(
        "app.models.products.core.products_model.Products", backref="clasp_types"
    )
