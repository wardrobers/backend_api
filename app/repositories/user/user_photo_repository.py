from typing import List
from sqlalchemy.orm import Session
from .models import UserPhoto
from .schemas import UserPhotoCreate

class UserPhotoRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_photo(self, photo_data: dict) -> UserPhoto:
        new_photo = UserPhoto(**photo_data)
        self.db.add(new_photo)
        self.db.commit()
        return new_photo

    def get_photos_by_user_uuid(self, user_uuid: str) -> List[UserPhoto]:
        return self.db.query(UserPhoto).filter(UserPhoto.user_uuid == user_uuid).all()

    def delete_photo(self, photo_uuid: str):
        photo = self.db.query(UserPhoto).filter(UserPhoto.uuid == photo_uuid).first()
        if photo:
            self.db.delete(photo)
            self.db.commit()

    def update_photo(self, photo_uuid: str, photo_data: dict) -> Optional[UserPhoto]:
        """Update a user photo's details."""
        photo = self.db.query(UserPhoto).filter(UserPhoto.uuid == photo_uuid).first()
        if photo:
            for key, value in photo_data.items():
                setattr(photo, key, value)
            self.db.commit()
            return photo
        return None
