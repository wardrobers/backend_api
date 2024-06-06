import os
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from google.cloud import storage
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserPhotos
from app.repositories.common import (
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)
from app.schemas.users import UserPhotoCreate, UserPhotoRead, UserPhotoUpdate


class UserPhotosRepository(BaseMixin, CachingMixin, BulkActionsMixin, SearchMixin):
    """
    Repository for managing user photos stored in Google Cloud Storage (GCS).
    Handles different environments (local, testing, production).
    """

    def __init__(self, db_session: AsyncSession, environment: str = "development"):
        self.db_session = db_session
        self.environment = environment
        self.gcp_bucket_name = os.environ.get("GCP_BUCKET_NAME")
        self.storage_client = (
            storage.Client() if self.environment == "production" else None
        )  # Only initialize in production
        self.model = UserPhotos

    async def get_user_photos(self, user_id: UUID) -> list[UserPhotoRead]:
        """Retrieves all photos for a given user."""
        async with self.db_session as session:
            photos = await session.execute(
                select(UserPhotos).where(UserPhotos.user_id == user_id)
            )
            return [
                UserPhotoRead.model_validate(photo)
                for photo in photos.scalars().all()
            ]

    async def get_user_photo_by_id(
        self, user_id: UUID, photo_id: UUID
    ) -> Optional[UserPhotoRead]:
        """Retrieves a specific photo by ID for a given user."""
        async with self.db_session as session:
            photo = await session.execute(
                select(UserPhotos).where(
                    UserPhotos.id == photo_id, UserPhotos.user_id == user_id
                )
            )
            photo = photo.scalars().first()
            return UserPhotoRead.model_validate(photo) if photo else None

    async def add_user_photo(
        self, user_id: UUID, photo_data: UserPhotoCreate
    ) -> UserPhotoRead:
        """Adds a new photo, uploading to GCS or saving locally."""
        async with self.db_session as session:
            new_photo = UserPhotos(
                user_id=user_id, image_url=photo_data.image_url
            )
            session.add(new_photo)
            await session.commit()
            await session.refresh(new_photo)
            return UserPhotoRead.model_validate(new_photo)

    async def update_user_photo(
        self, user_id: UUID, photo_id: UUID, photo_data: UserPhotoUpdate
    ) -> UserPhotoRead:
        """Updates a user's photo, potentially including re-uploading to storage."""
        async with self.db_session as session:
            photo = await self.get_user_photo_by_id(user_id, photo_id)
            if not photo:
                raise HTTPException(status_code=404, detail="Photo not found")

            if photo_data.image_url:  # Check if a new image is provided
                # Delete the old image from storage
                if self.environment == "production":
                    await self._delete_from_gcs(photo.image_url)
                else:
                    self._delete_locally(photo.image_url)

                # Upload the new image and update the URL
                filename = f"user_{user_id}/{photo_id}"
                photo.image_url = await self._upload_image(filename, photo_data.image_url)

            await photo.update(
                session, **photo_data.model_dump(exclude_unset=True)
            )
            await session.commit()
            await session.refresh(photo)
            return UserPhotoRead.model_validate(photo)

    async def delete_user_photo(self, user_id: UUID, photo_id: UUID) -> None:
        """Deletes a user's photo from the database and storage."""
        async with self.db_session as session:
            photo = await self.get_user_photo_by_id(user_id, photo_id)
            if not photo:
                raise HTTPException(status_code=404, detail="Photo not found")

            if self.environment == "production":
                await self._delete_from_gcs(photo.image_url)
            else:
                self._delete_locally(photo.image_url)

            await session.delete(photo)
            await session.commit()

    async def _upload_image(self, filename: str, image_data: UploadFile) -> str:
        """Handles image upload based on environment (GCS or local)."""
        if self.environment == "production":
            return await self._upload_to_gcs(filename, image_data)
        else:
            return self._save_locally(filename, image_data)

    async def _upload_to_gcs(self, filename: str, image_data: UploadFile) -> str:
        """Uploads the image to Google Cloud Storage."""
        bucket = self.storage_client.bucket(self.gcp_bucket_name)
        blob = bucket.blob(filename)

        # Upload from bytes (you'll need to get bytes from the UploadFile)
        image_bytes = await image_data.read()
        await blob.upload_from_string(
            image_bytes, content_type=image_data.content_type
        ) 
        blob.make_public()
        return f"https://storage.googleapis.com/{self.gcp_bucket_name}/{filename}"

    def _save_locally(self, filename: str, image_data: UploadFile) -> str:
        """Saves the image to the local filesystem."""
        image_dir = os.path.join(
            "media", "images"
        )  # Create 'media/images' if it doesn't exist
        os.makedirs(image_dir, exist_ok=True)
        filepath = os.path.join(image_dir, filename)

        # Save image from bytes
        with open(filepath, "wb") as f:
            f.write(image_data.read())
        return filepath

    async def _delete_from_gcs(self, image_url: str) -> None:
        """Deletes the image from Google Cloud Storage."""
        bucket = self.storage_client.bucket(self.gcp_bucket_name)
        blob = bucket.blob(image_url.split("/")[-1])
        await blob.delete()

    def _delete_locally(self, filepath: str) -> None:
        """Deletes the image from the local filesystem."""
        if os.path.exists(filepath):
            os.remove(filepath)