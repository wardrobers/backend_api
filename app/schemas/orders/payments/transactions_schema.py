from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field
from typing_extensions import Annotated

from app.schemas.orders import LenderPaymentRead


# --- Transactions Schemas (app/schemas/transactions.py) ---
class TransactionBase(BaseModel):
    amount: Annotated[Decimal, Field(..., description="The amount of the transaction.")]
    currency: str = Field(
        ..., description="The currency of the transaction (e.g., 'USD', 'EUR')."
    )
    transaction_date: datetime = Field(
        ..., description="The date and time of the transaction."
    )

    def get_transacation_status(self):
        from app.models.orders.payments.transactions_model import TransactionStatus

        return TransactionStatus

    status: get_transacation_status = Field(
        ..., description="The status of the transaction."
    )
    user_id: UUID4 = Field(
        ..., description="The ID of the user who made the transaction."
    )
    payment_method_id: UUID4 = Field(
        ..., description="The ID of the payment method used for the transaction."
    )
    order_id: UUID4 = Field(
        ..., description="The ID of the order associated with this transaction."
    )
    user_address_id: Optional[UUID4] = Field(
        None,
        description="The ID of the user's address associated with the transaction (if applicable).",
    )


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: UUID4
    # revolut_details: Optional["RevolutDetailsRead"] = None
    # stripe_details: Optional["StripeDetailsRead"] = None
    lender_payment: Optional[LenderPaymentRead] = None

    class Config:
        from_attributes = True


class TransactionUpdate(TransactionBase):
    amount: Optional[
        Annotated[Decimal, Field(description="The amount of the transaction.")]
    ] = None
    currency: Optional[str] = Field(
        None, description="The currency of the transaction (e.g., 'USD', 'EUR')."
    )
    transaction_date: Optional[datetime] = Field(
        None, description="The date and time of the transaction."
    )

    def get_transacation_status(self):
        from app.models.orders.payments.transactions_model import TransactionStatus

        return TransactionStatus

    status: Optional[get_transacation_status] = Field(
        None, description="The status of the transaction."
    )


# --- Resolving Forward References ---
TransactionRead.model_rebuild()
