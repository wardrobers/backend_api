from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field
from typing_extensions import Annotated

# --- LenderPayments ---


class LenderPaymentBase(BaseModel):
    payment_percentage: Annotated[
        Decimal,
        Field(
            ..., ge=0, le=100, description="Percentage of rental income paid to lender."
        ),
    ]
    payment_amount: Annotated[
        Decimal, Field(..., description="Amount paid to the lender.")
    ]
    # payment_status: PaymentStatus = Field(..., description="The status of the lender payment.")
    article_id: UUID4 = Field(
        ..., description="The ID of the article for which the payment is made."
    )
    transaction_id: UUID4 = Field(
        ..., description="The ID of the transaction associated with this payment."
    )


class LenderPaymentCreate(LenderPaymentBase):
    pass


class LenderPaymentRead(LenderPaymentBase):
    id: UUID4

    class Config:
        from_attributes = True


class LenderPaymentUpdate(LenderPaymentBase):
    payment_percentage: Optional[
        Annotated[
            Decimal,
            Field(
                ge=0, le=100, description="Percentage of rental income paid to lender."
            ),
        ]
    ] = None
    payment_amount: Optional[
        Annotated[Decimal, Field(description="Amount paid to the lender.")]
    ] = None
    # payment_status: Optional[PaymentStatus] = Field(None, description="The status of the lender payment.")


# --- Resolving Forward References ---
LenderPaymentRead.model_rebuild()
