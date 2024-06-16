from typing import Optional

from pydantic import BaseModel, UUID4, Field

from app.models.products.core.artices_model import OwnerType, Condition


# --- Articles ---

class ArticleBase(BaseModel):
    article: str = Field(..., description="A unique identifier or code for the article.")
    owner_type: OwnerType = Field(..., description="The type of owner of the article.")
    factory_number: Optional[str] = Field(None, description="The factory number of the article (if applicable).")
    times_used: int = Field(0, ge=0, description="The number of times the article has been rented.")
    hours_used: int = Field(0, ge=0, description="The number of hours the article has been used (if applicable).")
    min_rental_days: int = Field(2, ge=1, description="The minimum number of days the article can be rented for.")
    buffer_days: int = Field(1, ge=0, description="The number of buffer days before/after rentals.")
    pre_rental_buffer: int = Field(0, ge=0, description="Buffer days required before a rental starts.")
    for_cleaning: bool = Field(False, description="Indicates if the article is currently being cleaned.")
    for_repair: bool = Field(False, description="Indicates if the article is currently being repaired.")
    condition: Condition = Field(..., description="The current condition of the article.")
    sku_id: UUID4 = Field(..., description="The ID of the SKU this article belongs to.")
    status_code: UUID4 = Field(..., description="The ID of the article status code.")
    types_of_operation_id: UUID4 = Field(..., description="The ID of the type of operation allowed for this article.")


class ArticleCreate(ArticleBase):
    pass


class ArticleRead(ArticleBase):
    id: UUID4
    specification: Optional[SpecificationRead] = None
    cleaning_logs: Optional[list[CleaningLogRead]] = None
    repair_logs: Optional[list[RepairLogRead]] = None
    lender_payments: Optional[list[LenderPaymentRead]] = None
    order_items: Optional[list[LenderPaymentRead]] = None

    class Config:
        orm_mode = True


class ArticleUpdate(ArticleBase):
    article: Optional[str] = Field(None, description="A unique identifier or code for the article.")
    owner_type: Optional[OwnerType] = Field(None, description="The type of owner of the article.")
    factory_number: Optional[str] = Field(None, description="The factory number of the article (if applicable).")
    times_used: Optional[int] = Field(None, ge=0, description="The number of times the article has been rented.")
    hours_used: Optional[int] = Field(None, ge=0, description="The number of hours the article has been used (if applicable).")
    min_rental_days: Optional[int] = Field(None, ge=1, description="The minimum number of days the article can be rented for.")
    buffer_days: Optional[int] = Field(None, ge=0, description="The number of buffer days before/after rentals.")
    pre_rental_buffer: Optional[int] = Field(None, ge=0, description="Buffer days required before a rental starts.")
    for_cleaning: Optional[bool] = Field(None, description="Indicates if the article is currently being cleaned.")
    for_repair: Optional[bool] = Field(None, description="Indicates if the article is currently being repaired.")
    condition: Optional[Condition] = Field(None, description="The current condition of the article.")


# --- Resolving Forward References ---
ArticleRead.model_rebuild()