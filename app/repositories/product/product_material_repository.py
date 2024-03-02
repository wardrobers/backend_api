from sqlalchemy.orm import Session
from typing import Optional
from .models import ProductMaterial
from .schemas import ProductMaterialCreate, ProductMaterialUpdate
from pydantic import UUID4

class ProductMaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_product_materials(self, product_uuid: UUID4) -> list[ProductMaterial]:
        return (
            self.db.query(ProductMaterial)
            .filter(ProductMaterial.product_uuid == product_uuid)
            .all()
        )

    def add_material_to_product(self, product_material_data: ProductMaterialCreate) -> ProductMaterial:
        product_material = ProductMaterial(**product_material_data.dict())
        self.db.add(product_material)
        self.db.commit()
        self.db.refresh(product_material)
        return product_material

    def update_product_material(self, product_uuid: UUID4, material_uuid: UUID4, product_material_data: ProductMaterialUpdate) -> Optional[ProductMaterial]:
        product_material = (
            self.db.query(ProductMaterial)
            .filter(
                ProductMaterial.product_uuid == product_uuid,
                ProductMaterial.material_uuid == material_uuid,
            )
            .first()
        )
        if product_material:
            for key, value in product_material_data.dict(exclude_unset=True).items():
                setattr(product_material, key, value)
            self.db.commit()
            return product_material
        return None

    def remove_material_from_product(self, product_uuid: UUID4, material_uuid: UUID4) -> None:
        product_material = (
            self.db.query(ProductMaterial)
            .filter(
                ProductMaterial.product_uuid == product_uuid,
                ProductMaterial.material_uuid == material_uuid,
            )
            .first()
        )
        if product_material:
            self.db.delete(product_material)
            self.db.commit()

    def list_all_product_materials(self) -> list[ProductMaterial]:
        return self.db.query(ProductMaterial).all()
