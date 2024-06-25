from typing import Optional

from pydantic import UUID4, BaseModel

from app.schemas.products.sizing.size_systems_schema import SizeSystemRead

# --- Sizing ---


class SizingBase(BaseModel):
    label: str
    measurements: Optional[dict] = None
    variant_id: UUID4
    size_system_id: UUID4


class SizingCreate(SizingBase):
    pass


class SizingRead(SizingBase):
    id: UUID4
    size_system: SizeSystemRead


class SizingUpdate(SizingBase):
    label: Optional[str] = None
    measurements: Optional[dict] = None


# --- Resolving Forward References ---
SizingRead.model_rebuild()
SizingCreate.model_rebuild()
