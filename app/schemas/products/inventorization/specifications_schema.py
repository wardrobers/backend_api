from typing import Optional

from pydantic import BaseModel, UUID4, Field


# --- Specifications ---

class SpecificationBase(BaseModel):
    name: str = Field(..., description="The name of the specification.")
    index: int = Field(..., description="An index to order the specifications.")
    value: str = Field(..., description="The value of the specification.")
    article_id: UUID4 = Field(..., description="The ID of the article this specification belongs to.")


class SpecificationCreate(SpecificationBase):
    pass


class SpecificationRead(SpecificationBase):
    id: UUID4

    class Config:
        from_attributes = True


class SpecificationUpdate(SpecificationBase):
    name: Optional[str] = Field(None, description="The name of the specification.")
    index: Optional[int] = Field(None, description="An index to order the specifications.")
    value: Optional[str] = Field(None, description="The value of the specification.")


# --- Resolving Forward References ---
SpecificationRead.model_rebuild()