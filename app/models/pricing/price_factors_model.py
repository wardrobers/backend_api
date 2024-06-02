from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class PriceFactors(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "price_factors"

    rental_period = Column(Numeric, nullable=False)
    percentage = Column(Numeric, nullable=False)

    # Foreign keys
    pricing_tier_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("pricing_tiers.id"),
        nullable=False,
    )
