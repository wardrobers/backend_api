from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class Colors(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "colors"

    name = Column(String)

    # Relationships
    variant = relationship(
        "app.models.products.core.variants_model.Variants", backref="colors"
    )
