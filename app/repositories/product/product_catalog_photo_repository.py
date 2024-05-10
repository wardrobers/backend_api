from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from ...models.products.product_catalog_photo_model import ProductsCatalogPhoto
from ...schemas.product.product_catalog_photo_schema import (
    ProductsCatalogPhotoCreate,
    ProductsCatalogPhotoUpdate,
)


class ProductsCatalogPhotoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_products_catalog_photo(
        self, photo_data: ProductsCatalogPhotoCreate
    ) -> ProductsCatalogPhoto:
        new_photo = ProductsCatalogPhoto(**photo_data.dict())
        self.db.add(new_photo)
        self.db.commit()
        self.db.refresh(new_photo)
        return new_photo

    def get_products_catalog_photo(self, uuid: UUID) -> Optional[ProductsCatalogPhoto]:
        return (
            self.db.query(ProductsCatalogPhoto)
            .filter(ProductsCatalogPhoto.id == uuid)
            .first()
        )

    def list_products_catalog_photos(
        self, skip: int = 0, limit: int = 100
    ) -> list[ProductsCatalogPhoto]:
        return self.db.query(ProductsCatalogPhoto).offset(skip).limit(limit).all()

    def update_products_catalog_photo(
        self, uuid: UUID, update_data: ProductsCatalogPhotoUpdate
    ) -> Optional[ProductsCatalogPhoto]:
        photo = self.get_products_catalog_photo(uuid)
        if photo:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(photo, key, value)
            self.db.commit()
            self.db.refresh(photo)
            return photo
        return None

    def delete_products_catalog_photo(self, uuid: UUID) -> None:
        photo = self.get_products_catalog_photo(uuid)
        if photo:
            self.db.delete(photo)
            self.db.commit()

    def set_showcase_for_product(self, product_id: UUID, photo_id: UUID) -> None:
        # Assuming there could be multiple photos but only one showcase at a time
        photos = (
            self.db.query(ProductsCatalogPhoto)
            .filter(ProductsCatalogPhoto.product_id == product_id)
            .all()
        )
        for photo in photos:
            photo.showcase = photo.id == photo_id
        self.db.commit()
