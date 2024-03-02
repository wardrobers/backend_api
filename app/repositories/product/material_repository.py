from typing import Optional
from pydantic import UUID4
from sqlalchemy.orm import Session
from .models import Material
from .schemas import MaterialCreate, MaterialUpdate


class MaterialRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_material_by_uuid(self, uuid: UUID4) -> Optional[Material]:
        return self.db.query(Material).filter(Material.uuid == uuid).first()

    def create_material(self, material_data: MaterialCreate) -> Material:
        new_material = Material(**material_data.dict())
        self.db.add(new_material)
        self.db.commit()
        self.db.refresh(new_material)
        return new_material

    def update_material(self, uuid: UUID4, material_data: MaterialUpdate) -> Optional[Material]:
        material = self.get_material_by_uuid(uuid)
        if material:
            for key, value in material_data.dict(exclude_unset=True).items():
                setattr(material, key, value)
            self.db.commit()
            return material
        return None

    def delete_material(self, uuid: UUID4):
        material = self.get_material_by_uuid(uuid)
        if material:
            self.db.delete(material)
            self.db.commit()