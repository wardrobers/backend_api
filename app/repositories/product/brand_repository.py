from typing import Optional
from pydantic import UUID4
from sqlalchemy.orm import Session
from .models import Brand
from .schemas import BrandCreate, BrandUpdate


class BrandRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_brand_by_uuid(self, uuid: UUID4) -> Optional[Brand]:
        return self.db.query(Brand).filter(Brand.uuid == uuid).first()

    def create_brand(self, brand_data: BrandCreate) -> Brand:
        new_brand = Brand(**brand_data.dict())
        self.db.add(new_brand)
        self.db.commit()
        self.db.refresh(new_brand)
        return new_brand

    def update_brand(self, uuid: UUID4, brand_data: BrandUpdate) -> Optional[Brand]:
        brand = self.get_brand_by_uuid(uuid)
        if brand:
            for key, value in brand_data.dict(exclude_unset=True).items():
                setattr(brand, key, value)
            self.db.commit()
            return brand
        return None

    def delete_brand(self, uuid: UUID4):
        brand = self.get_brand_by_uuid(uuid)
        if brand:
            self.db.delete(brand)
            self.db.commit()