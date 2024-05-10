from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime


class MaterialBase(BaseModel):
    name: Optional[str]


class MaterialRead(MaterialBase):
    uuid: UUID4
    name: Optional[str]
    product_type_id: UUID4
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


class MaterialCreate(BaseModel):
    name: str = Field(..., description="The name of the material.")
    product_type_id: UUID4 = Field(
        ..., description="The UUID of the associated product type."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Cotton",
                "product_type_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }


class MaterialUpdate(BaseModel):
    name: Optional[str] = Field(None, description="The name of the material.")
    product_type_id: Optional[UUID4] = Field(
        None, description="The UUID of the associated product type."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Cotton",
                "product_type_id": "123e4567-e89b-12d3-a456-426614174000",
            }
        }
