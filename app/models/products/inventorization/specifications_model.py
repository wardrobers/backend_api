from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class Specifications(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "specifications"

    name = Column(String)
    index = Column(Integer)
    value = Column(String)

    # Foreign keys
    article_id = mapped_column(String, ForeignKey("articles.id"), nullable=False)
