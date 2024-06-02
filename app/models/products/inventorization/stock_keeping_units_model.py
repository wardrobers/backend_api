from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class StockKeepingUnits(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "stock_keeping_units"

    free_articles_count = Column(Integer, nullable=False, server_default=0)
    sku_name = Column(String, nullable=False)

    # Relationships
    articles = relationship(
        "app.models.products.core.articles_model.Articles",
        backref="stock_keeping_units",
    )
    variants = relationship(
        "app.models.products.core.variants_model.Variants",
        backref="stock_keeping_units",
    )
    user_basket = relationship(
        "app.models.users.activity.user_basket_model.UserBasket",
        backref="stock_keeping_units",
    )
    pricing_tiers = relationship(
        "app.models.pricing.pricing_tiers_model.PricingTiers",
        backref="stock_keeping_unit",
    )
