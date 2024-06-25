from typing import Optional

from pydantic import UUID4, BaseModel

from app.schemas.products.core.variants_schema import VariantCreate, VariantRead
from app.schemas.products.inventorization.categories_schema import CategoryRead
from app.schemas.products.product_details.brand_schema import BrandRead

# --- Products ---


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    brand_id: UUID4
    clothing_size_id: Optional[UUID4] = None
    clasp_type_id: Optional[UUID4] = None
    size_and_fit_id: Optional[UUID4] = None
    status_code: UUID4
    accessories_size_id: Optional[UUID4] = None
    variants: Optional[list[VariantCreate]] = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: UUID4
    variants: list[VariantRead] = []
    brand: BrandRead
    categories: list[CategoryRead] = []


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    variants: Optional[list[VariantCreate]] = None


# --- Resolving Forward References ---
ProductRead.model_rebuild()
