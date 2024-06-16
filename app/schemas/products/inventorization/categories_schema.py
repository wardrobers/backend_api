from typing import Optional

from pydantic import UUID4, BaseModel

from app.schemas.products.product_details.materials_schema import MaterialRead

# --- Categories ---


class CategoryBase(BaseModel):
    name: str
    is_default: bool = False


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: UUID4
    materials: list[MaterialRead] = []


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    is_default: Optional[bool] = None


# --- Resolving Forward References ---
CategoryRead.model_rebuild()
CategoryCreate.model_rebuild()
