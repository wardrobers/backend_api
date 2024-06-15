from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class StockKeepingUnits(Base):
    __tablename__ = "stock_keeping_units"

    free_articles_count = Column(Integer, nullable=False, default=0)
    sku_name = Column(String, nullable=False)

    # Relationships
    articles = relationship(
        "Articles",
        backref="stock_keeping_units",
        cascade="all, delete-orphan",
    )
    variants = relationship(
        "Variants",
        backref="stock_keeping_units",
    )
    user_basket = relationship(
        "UserBasket",
        backref="stock_keeping_units",
    )
    pricing_tiers = relationship(
        "PricingTiers",
        backref="stock_keeping_units",
    )
