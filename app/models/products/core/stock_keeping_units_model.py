from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class StockKeepingUnits(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "stock_keeping_units"

    free_articles_count = Column(Integer, nullable=False, server_default=0)
    sku_name = Column(String, nullable=False)

    # Relationships
    articles = relationship("Articles", backref="stock_keeping_units")
    variants = relationship("Variants", backref="stock_keeping_units")
    user_basket = relationship("UserBasket", backref="stock_keeping_units")
    pricing_tiers = relationship("PricingTiers", backref="stock_keeping_unit")
