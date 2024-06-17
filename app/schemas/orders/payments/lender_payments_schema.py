from typing import Optional

from pydantic import BaseModel, UUID4, Field
from typing_extensions import Annotated


# --- LenderPayments ---

class LenderPaymentBase(BaseModel):
    payment_percentage: Annotated[int, Field(..., ge=0, le=100, description="Percentage of rental income paid to lender.")]
    payment_amount: Annotated[int, Field(..., description="Amount paid to the lender.", decimal_places=2)]
    # payment_status: PaymentStatus = Field(..., description="The status of the lender payment.")
    article_id: UUID4 = Field(..., description="The ID of the article for which the payment is made.")
    transaction_id: UUID4 = Field(..., description="The ID of the transaction associated with this payment.")


class LenderPaymentCreate(LenderPaymentBase):
    pass


class LenderPaymentRead(LenderPaymentBase):
    id: UUID4

    class Config:
        orm_mode = True


class LenderPaymentUpdate(LenderPaymentBase):
    payment_percentage: Optional[Annotated[int, Field(ge=0, le=100, description="Percentage of rental income paid to lender.")]] = None
    payment_amount: Optional[Annotated[int, Field(description="Amount paid to the lender.", decimal_places=2)]] = None
    # payment_status: Optional[PaymentStatus] = Field(None, description="The status of the lender payment.")


# --- Resolving Forward References ---
LenderPaymentRead.model_rebuild()