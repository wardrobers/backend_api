from typing import Optional
from sqlalchemy.orm import Session
from ...models.user.user_photo_model import UsersPhotos
from ...schemas.user.user_photo_schema import UserPhotoCreate


class UserPhotoRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_photo(self, photo_data: dict) -> UsersPhotos:
        new_photo = UsersPhotos(**photo_data)
        self.db.add(new_photo)
        self.db.commit()
        return new_photo

    def get_photos_by_user_uuid(self, user_uuid: str) -> list[UsersPhotos]:
        return (
            self.db.query(UsersPhotos).filter(UsersPhotos.user_uuid == user_uuid).all()
        )

    def delete_photo(self, photo_uuid: str):
        photo = (
            self.db.query(UsersPhotos).filter(UsersPhotos.uuid == photo_uuid).first()
        )
        if photo:
            self.db.delete(photo)
            self.db.commit()

    def update_photo(self, photo_uuid: str, photo_data: dict) -> Optional[UsersPhotos]:
        """Update a user photo's details."""
        photo = (
            self.db.query(UsersPhotos).filter(UsersPhotos.uuid == photo_uuid).first()
        )
        if photo:
            for key, value in photo_data.items():
                setattr(photo, key, value)
            self.db.commit()
            return photo
        return None
