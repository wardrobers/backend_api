from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, UUID4, Field
from typing_extensions import Annotated

# --- PricingTiers ---

class PricingTierBase(BaseModel):
    retail_price: Annotated[Decimal, Field(..., description="The base retail price of the product.", decimal_places=2)]
    max_price_threshold: Optional[Annotated[Decimal, Field(description="The maximum price threshold for applying discounts.", decimal_places=2)]] = None
    max_price_discount: Optional[Annotated[Decimal, Field(description="The maximum discount that can be applied to the price.", decimal_places=2)]] = None
    additional_discount: Optional[Annotated[Decimal, Field(description="Any additional discount that can be applied.", decimal_places=2)]] = None
    tax_percentage: Annotated[Decimal, Field(..., description="The percentage of tax to be applied to the price.", decimal_places=2)]
    insurance: Optional[Annotated[Decimal, Field(description="The cost of insurance for the product (if applicable).", decimal_places=2)]] = None
    cleaning: Optional[Annotated[Decimal, Field(description="The cleaning fee for the product (if applicable).", decimal_places=2)]] = None
    sku_id: UUID4 = Field(..., description="The ID of the SKU this pricing tier applies to.")
    price_multiplier_id: UUID4 = Field(..., description="The ID of the price multiplier for this tier.")


class PricingTierCreate(PricingTierBase):
    pass


class PricingTierRead(PricingTierBase):
    id: UUID4
    price_factors: Optional[list[PriceFactorRead]] = None

    class Config:
        orm_mode = True


class PricingTierUpdate(PricingTierBase):
    retail_price: Optional[Annotated[Decimal, Field(description="The base retail price of the product.", decimal_places=2)]] = None
    max_price_threshold: Optional[Annotated[Decimal, Field(description="The maximum price threshold for applying discounts.", decimal_places=2)]] = None
    max_price_discount: Optional[Annotated[Decimal, Field(description="The maximum discount that can be applied to the price.", decimal_places=2)]] = None
    additional_discount: Optional[Annotated[Decimal, Field(description="Any additional discount that can be applied.", decimal_places=2)]] = None
    tax_percentage: Optional[Annotated[Decimal, Field(description="The percentage of tax to be applied to the price.", decimal_places=2)]] = None
    insurance: Optional[Annotated[Decimal, Field(description="The cost of insurance for the product (if applicable).", decimal_places=2)]] = None
    cleaning: Optional[Annotated[Decimal, Field(description="The cleaning fee for the product (if applicable).", decimal_places=2)]] = None


# --- Resolving Forward References ---
PricingTierRead.model_rebuild()