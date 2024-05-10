from sqlalchemy import ForeignKey, JSON, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class CategoriesForUser(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "categories_for_user"

    coefficient = Column(String)
    raw = Column(JSON)

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = mapped_column(UUID(as_uuid=True), ForeignKey("types.id"))
