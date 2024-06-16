from typing import Optional

from pydantic import UUID4, BaseModel

from app.schemas.products.product_details.colors_schema import ColorRead
from app.schemas.products.sizing.sizing_schema import SizingCreate, SizingRead

# --- Variants ---


class VariantBase(BaseModel):
    name: str
    index: Optional[int] = None
    product_id: UUID4
    sku_id: UUID4
    color_id: UUID4


class VariantCreate(VariantBase):
    sizing: list[SizingCreate] = []


class VariantRead(VariantBase):
    id: UUID4
    color: ColorRead
    sizing: list[SizingRead] = []


class VariantUpdate(VariantBase):
    name: Optional[str] = None
    index: Optional[int] = None
    sizing: Optional[list[SizingCreate]] = None


# --- Resolving Forward References ---
VariantRead.model_rebuild()
