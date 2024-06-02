from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class Specifications(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "specifications"

    name = Column(String)
    index = Column(Integer)
    value = Column(String)

    # Foreign keys
    article_id = mapped_column(String, ForeignKey("articles.id"), nullable=False)
