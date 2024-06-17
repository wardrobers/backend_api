from typing import Optional

from pydantic import BaseModel, UUID4, Field
from app.schemas.products import ArticleRead, VariantRead
from app.schemas.users import UserBasketRead
from app.schemas.pricing import PricingTierRead


# --- StockKeepingUnits ---
class StockKeepingUnitBase(BaseModel):
    free_articles_count: int = Field(
        ..., ge=0, description="The number of free (available) articles for this SKU."
    )
    sku_name: str = Field(..., description="The unique name or code for this SKU.")


class StockKeepingUnitCreate(StockKeepingUnitBase):
    pass


class StockKeepingUnitRead(StockKeepingUnitBase):
    id: UUID4
    articles: Optional[list[ArticleRead]] = None
    variants: Optional[list[VariantRead]] = None
    user_basket: Optional[list[UserBasketRead]] = None
    pricing_tiers: Optional[list[PricingTierRead]] = None

    class Config:
        from_attributes = True


class StockKeepingUnitUpdate(StockKeepingUnitBase):
    free_articles_count: Optional[int] = Field(
        None, ge=0, description="The number of free (available) articles for this SKU."
    )
    sku_name: Optional[str] = Field(
        None, description="The unique name or code for this SKU."
    )
