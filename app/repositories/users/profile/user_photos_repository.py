import os

from fastapi import HTTPException, UploadFile
from google.cloud import storage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import UUID

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

    async def add_user_photo(self, user_id: UUID, photo_data: UploadFile) -> UserPhotos:
        """Adds a new photo for the user, uploading it to GCS or simulating for local/testing."""

        filename = f"user_{user_id}/{photo_data.filename}"

        if self.environment == "production":
            # Upload to GCS in production
            await self._upload_to_gcs(filename, photo_data)
            image_url = (
                f"https://storage.googleapis.com/{self.gcp_bucket_name}/{filename}"
            )
        else:
            # Simulate upload for local/testing
            image_url = f"/images/{filename}"  # Or any other placeholder URL

        # Create the photo object in the database
        new_photo = UserPhotos(user_id=user_id, image_url=image_url)
        self.db_session.add(new_photo)
        await self.db_session.commit()
        await self.db_session.refresh(new_photo)

        return new_photo

    async def _upload_to_gcs(self, filename: str, photo_data: UploadFile):
        """Uploads the photo data to GCS."""
        bucket = self.storage_client.bucket(self.gcp_bucket_name)
        blob = bucket.blob(filename)
        await blob.upload_from_file(
            photo_data.file, content_type=photo_data.content_type
        )
        blob.make_public()  # Make the photo publicly accessible

    async def delete_user_photo(self, user_id: UUID, photo_id: UUID) -> None:
        """
        Deletes a user's photo from the database and GCS (or simulates for local/testing).
        """
        photo = await self.db_session.execute(
            select(UserPhotos).where(
                UserPhotos.id == photo_id, UserPhotos.user_id == user_id
            )
        )
        photo = photo.scalars().first()
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        if self.environment == "production":
            # Delete from GCS in production
            bucket = self.storage_client.bucket(self.gcp_bucket_name)
            blob = bucket.blob(photo.image_url.split("/")[-1])
            blob.delete()
        else:
            # Simulate deletion for local/testing
            pass  # No actual deletion needed in this environment

        # Delete the photo record from the database
        await self.db_session.delete(photo)
        await self.db_session.commit()
