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

    async def add_user_photo(
        self, user_id: UUID, photo_data: UploadFile
    ) -> UserPhotos:
        """Adds a new photo for the user, performing checks and logic."""

        # Example of complex logic:
        # - Check if the user has reached the maximum allowed number of photos.
        # - Resize/compress the image before uploading.
        # - Generate thumbnails.
        # ...

        return await self.user_photo_repository.add_user_photo(user_id, photo_data)

    async def delete_user_photo(self, user_id: UUID, photo_id: UUID) -> None:
        """Deletes a user photo, handling authorization and additional logic."""

        # Example of complex logic:
        # - Check if the user is authorized to delete the photo (ownership, permissions).
        # - Perform any necessary cleanup (e.g., deleting thumbnails).
        # ...

        await self.user_photo_repository.delete_user_photo(user_id, photo_id)
