import os
from typing import Optional

from fastapi import HTTPException, UploadFile
from google.cloud import storage
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserPhotos
from app.schemas.users import UserPhotoRead


class UserPhotosRepository:
    """
    Repository for managing user photos stored in Google Cloud Storage (GCS).
    Handles different environments (local, testing, production).
    """

    def __init__(self, db_session: AsyncSession, environment: str = "development"):
        self.db_session = db_session
        self.environment = environment
        self.gcp_bucket_name = os.environ.get("GCP_BUCKET_NAME")
        self.storage_client = (
            storage.Client()
        )  # For production and potentially testing (if using a real bucket)

    async def get_user_photos(self, user_id: UUID) -> list[UserPhotoRead]:
        """Retrieves all photos for a given user."""
        photos = await self.db_session.execute(
            select(UserPhotos).where(UserPhotos.user_id == user_id)
        )
        return [
            UserPhotoRead(id=photo.id, user_id=photo.user_id, image_url=photo.image_url)
            for photo in photos.scalars().all()
        ]

    async def add_user_photo(
        self, user_id: UUID, photo_data: UploadFile, image: bytes
    ) -> UserPhotos:
        """Adds a new photo, uploading to GCS or saving locally."""
        filename = f"user_{user_id}/{photo_data.filename}"
        image_url = await self._upload_image(filename, image)

        new_photo = UserPhotos(user_id=user_id, image_url=image_url)
        self.db_session.add(new_photo)
        await self.db_session.commit()
        await self.db_session.refresh(new_photo)
        return new_photo

    async def _upload_image(self, filename: str, image: bytes) -> str:
        """Handles image upload based on environment (GCS or local)."""
        if self.environment == "production":
            return await self._upload_to_gcs(filename, image)
        else:
            return self._save_locally(filename, image)

    async def _upload_to_gcs(self, filename: str, image: bytes) -> str:
        """Uploads the image to Google Cloud Storage."""
        bucket = self.storage_client.bucket(self.gcp_bucket_name)
        blob = bucket.blob(filename)

        # Upload from bytes
        await blob.upload_from_string(
            image, content_type="image/jpeg"
        )  # Assuming JPEG after processing
        blob.make_public()
        return f"https://storage.googleapis.com/{self.gcp_bucket_name}/{filename}"

    def _save_locally(self, filename: str, image: bytes) -> str:
        """Saves the image to the local filesystem."""
        image_dir = os.path.join(
            "media", "images"
        )  # Create 'media/images' if it doesn't exist
        os.makedirs(image_dir, exist_ok=True)
        filepath = os.path.join(image_dir, filename)

        # Save image from bytes
        with open(filepath, "wb") as f:
            f.write(image)
        return filepath

    async def delete_user_photo(self, user_id: UUID, photo_id: UUID) -> None:
        """Deletes a user's photo from the database and storage."""
        photo: Optional[UserPhotos] = await self.db_session.execute(
            select(UserPhotos).where(
                UserPhotos.id == photo_id, UserPhotos.user_id == user_id
            )
        )
        photo = photo.scalars().first()
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        if self.environment == "production":
            await self._delete_from_gcs(photo.image_url)
        else:
            self._delete_locally(photo.image_url)

        await self.db_session.delete(photo)
        await self.db_session.commit()

    async def _delete_from_gcs(self, image_url: str) -> None:
        """Deletes the image from Google Cloud Storage."""
        bucket = self.storage_client.bucket(self.gcp_bucket_name)
        blob = bucket.blob(image_url.split("/")[-1])
        blob.delete()

    def _delete_locally(self, filepath: str) -> None:
        """Deletes the image from the local filesystem."""
        if os.path.exists(filepath):
            os.remove(filepath)
