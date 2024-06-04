# app/services/users/user_service.py
from fastapi import UploadFile
from sqlalchemy.orm import UUID

from app.models.users import UserPhotos
from app.repositories.users import UserPhotosRepository
from app.schemas.users import UserPhotoRead


class UserPhotosService:
    """
    Service layer for core user management operations.
    """

    def __init__(
        self,
        user_photo_repository: UserPhotosRepository,
    ):
        self.user_photo_repository = user_photo_repository

    # --- User Photo Operations ---
    async def get_user_photos(self, user_id: UUID) -> list[UserPhotoRead]:
        """Retrieves all photos for a user."""
        return await self.user_photo_repository.get_user_photos(user_id)

    async def add_user_photo(self, user_id: UUID, photo_data: UploadFile) -> UserPhotos:
        """Adds a new photo for the user."""
        return await self.user_photo_repository.add_user_photo(user_id, photo_data)

    async def delete_user_photo(self, user_id: UUID, photo_id: UUID) -> None:
        """Deletes a photo for the user."""
        await self.user_photo_repository.delete_user_photo(user_id, photo_id)
