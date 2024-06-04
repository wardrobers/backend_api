# app/services/users/user_service.py
import cv2
import numpy as np
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.dialects.postgresql import UUID

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
    ) -> UserPhotoRead:
        """
        Adds a new photo for the user, handling image processing and upload.

        Performs:
            - Image type validation.
            - Image resizing/compression.
            - Upload to GCS or local storage depending on the environment.
        """
        # Validate image type
        allowed_types = ["image/jpeg", "image/png"]
        if photo_data.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only JPEG and PNG images are allowed",
            )

        # Process image (resize/compress)
        image_bytes = await photo_data.read()
        image_np = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        image = self._process_image(image)

        # Upload image and create database record
        new_photo = await self.user_photo_repository.add_user_photo(
            user_id, photo_data, image
        )
        return UserPhotoRead.model_validate(new_photo)

    async def delete_user_photo(self, user_id: UUID, photo_id: UUID) -> None:
        """Deletes a user photo, including storage cleanup."""
        await self.user_photo_repository.delete_user_photo(user_id, photo_id)

    def _process_image(self, image: np.ndarray) -> bytes:
        """
        Processes the image using OpenCV: resize and compress.
        """
        max_size = (800, 600)  # Example max dimensions
        h, w = image.shape[:2]
        if h > max_size[1] or w > max_size[0]:
            interpolation = (
                cv2.INTER_AREA
                if h > max_size[1] and w > max_size[0]
                else cv2.INTER_CUBIC
            )
            image = cv2.resize(image, max_size, interpolation=interpolation)

        # Compress image to JPEG format
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]  # Set JPEG quality to 85
        _, encoded_image = cv2.imencode(".jpg", image, encode_param)
        return encoded_image.tobytes()
