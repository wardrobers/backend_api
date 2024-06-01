from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class StockKeepingUnits(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "stock_keeping_units"

    free_articles_count = Column(Integer, nullable=False, server_default=0)
    sku_name = Column(String, nullable=False)

    # Relationships
    articles = relationship("Articles", backref="stock_keeping_units")
    variants = relationship("Variants", backref="stock_keeping_units")
    user_basket = relationship("UserBasket", backref="stock_keeping_units")
    pricing_tiers = relationship("PricingTiers", backref='stock_keeping_unit')
