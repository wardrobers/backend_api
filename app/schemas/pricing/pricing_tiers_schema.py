from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field
from typing_extensions import Annotated

# --- PricingTiers ---


class PricingTierBase(BaseModel):
    retail_price: Annotated[
        Decimal, Field(..., description="The base retail price of the product.")
    ]
    max_price_threshold: Optional[
        Annotated[
            Decimal,
            Field(description="The maximum price threshold for applying discounts."),
        ]
    ] = None
    max_price_discount: Optional[
        Annotated[
            Decimal,
            Field(description="The maximum discount that can be applied to the price."),
        ]
    ] = None
    additional_discount: Optional[
        Annotated[
            Decimal, Field(description="Any additional discount that can be applied.")
        ]
    ] = None
    tax_percentage: Annotated[
        Decimal,
        Field(..., description="The percentage of tax to be applied to the price."),
    ]
    insurance: Optional[
        Annotated[
            Decimal,
            Field(description="The cost of insurance for the product (if applicable)."),
        ]
    ] = None
    cleaning: Optional[
        Annotated[
            Decimal,
            Field(description="The cleaning fee for the product (if applicable)."),
        ]
    ] = None
    sku_id: UUID4 = Field(
        ..., description="The ID of the SKU this pricing tier applies to."
    )
    price_multiplier_id: UUID4 = Field(
        ..., description="The ID of the price multiplier for this tier."
    )


class PricingTierCreate(PricingTierBase):
    pass


class PricingTierRead(PricingTierBase):
    id: UUID4
    # price_factors: Optional[list[PriceFactorRead]] = None

    class Config:
        from_attributes = True


class PricingTierUpdate(PricingTierBase):
    retail_price: Optional[
        Annotated[Decimal, Field(description="The base retail price of the product.")]
    ] = None
    max_price_threshold: Optional[
        Annotated[
            Decimal,
            Field(description="The maximum price threshold for applying discounts."),
        ]
    ] = None
    max_price_discount: Optional[
        Annotated[
            Decimal,
            Field(description="The maximum discount that can be applied to the price."),
        ]
    ] = None
    additional_discount: Optional[
        Annotated[
            Decimal, Field(description="Any additional discount that can be applied.")
        ]
    ] = None
    tax_percentage: Optional[
        Annotated[
            Decimal,
            Field(description="The percentage of tax to be applied to the price."),
        ]
    ] = None
    insurance: Optional[
        Annotated[
            Decimal,
            Field(description="The cost of insurance for the product (if applicable)."),
        ]
    ] = None
    cleaning: Optional[
        Annotated[
            Decimal,
            Field(description="The cleaning fee for the product (if applicable)."),
        ]
    ] = None


# --- Resolving Forward References ---
PricingTierRead.model_rebuild()
