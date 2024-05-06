from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from ...models.products.product_details.product_photos_model import ProductPhoto
from ...schemas.product.product_photo_schema import (
    ProductPhotoCreate,
    ProductPhotoRead,
    ProductPhotoUpdate,
)


class ProductPhotoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product_photo(self, photo_data: ProductPhotoCreate) -> ProductPhoto:
        new_photo = ProductPhoto(**photo_data.dict())
        self.db.add(new_photo)
        self.db.commit()
        self.db.refresh(new_photo)
        return new_photo

    def get_product_photo(self, uuid: UUID) -> Optional[ProductPhoto]:
        return self.db.query(ProductPhoto).filter(ProductPhoto.uuid == uuid).first()

    def list_product_photos(
        self, product_uuid: UUID, skip: int = 0, limit: int = 100
    ) -> List[ProductPhoto]:
        return (
            self.db.query(ProductPhoto)
            .filter(ProductPhoto.product_uuid == product_uuid)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_product_photo(
        self, uuid: UUID, update_data: ProductPhotoUpdate
    ) -> Optional[ProductPhoto]:
        photo = self.get_product_photo(uuid)
        if photo:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(photo, key, value)
            self.db.commit()
            self.db.refresh(photo)
            return photo
        return None

    def delete_product_photo(self, uuid: UUID) -> None:
        photo = self.get_product_photo(uuid)
        if photo:
            self.db.delete(photo)
            self.db.commit()

    def set_showcase_photo(self, product_uuid: UUID, photo_uuid: UUID) -> None:
        # Reset showcase status for all photos of the product
        photos = self.list_product_photos(product_uuid)
        for photo in photos:
            photo.showcase = photo.uuid == photo_uuid
        self.db.commit()

    # This method could be useful for scenarios where you might want to toggle the showcase status instead of setting it directly
    def toggle_showcase_photo(self, photo_uuid: UUID) -> None:
        photo = self.get_product_photo(photo_uuid)
        if photo:
            photo.showcase = not photo.showcase
            self.db.commit()
