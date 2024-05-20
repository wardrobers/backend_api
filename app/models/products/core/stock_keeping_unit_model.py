from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)


class StockKeepingUnit(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "stock_keeping_unit"

    sku_product = Column(String, nullable=False)
    sku_article = Column(String, nullable=False)

    # Relationships
    articles = relationship("Articles", backref="stock_keeping_unit")
    variants = relationship("Variants", backref="stock_keeping_unit")
    user_basket = relationship("UserBasket", backref="stock_keeping_unit")
