from typing import Optional

from pydantic import BaseModel, UUID4, Field

from app.models.products.inventorization.product_status_model import ProductCurrentStatus
from app.schemas.products import ProductRead


# --- ProductStatus ---
class ProductStatusBase(BaseModel):
    name: ProductCurrentStatus = Field(
        ..., description="The current status of the product."
    )


class ProductStatusCreate(ProductStatusBase):
    pass


class ProductStatusRead(ProductStatusBase):
    id: UUID4
    products: Optional[list[ProductRead]] = None
    class Config:
        orm_mode = True


class ProductStatusUpdate(ProductStatusBase):
    name: Optional[ProductCurrentStatus] = Field(
        None, description="The current status of the product."
    )