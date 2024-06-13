import os
from typing import Optional

from fastapi import HTTPException, UploadFile, status
from google.cloud import storage
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.models.users import UserPhotos
from app.repositories.common import BulkActionsMixin, CachingMixin, SearchMixin
from app.schemas.users import UserPhotoCreate, UserPhotoRead, UserPhotoUpdate


class UserPhotosRepository(CachingMixin, BulkActionsMixin, SearchMixin):
    """
    Repository for managing user photos stored in Google Cloud Storage (GCS).
    Handles different environments (local, testing, production).
    """

    def __init__(self, db_session: Session, environment: str = "development"):
        self.db_session = db_session
        self.environment = environment
        self.gcp_bucket_name = os.environ.get("GCP_BUCKET_NAME")
        self.storage_client = (
            storage.Client() if self.environment == "production" else None
        )  # Only initialize in production
        self.model = UserPhotos

    def get_user_photos(self, user_id: UUID) -> list[UserPhotoRead]:
        """Retrieves all photos for a given user."""

        photos = self.db_session.execute(
            select(UserPhotos).where(UserPhotos.user_id == user_id)
        )
        return [UserPhotoRead.model_validate(photo) for photo in photos.scalars().all()]

    def get_user_photo_by_id(
        self, user_id: UUID, photo_id: UUID
    ) -> Optional[UserPhotoRead]:
        """Retrieves a specific photo by ID for a given user."""

        photo = self.db_session.execute(
            select(UserPhotos).where(
                UserPhotos.id == photo_id, UserPhotos.user_id == user_id
            )
        )
        photo = photo.scalars().first()
        return UserPhotoRead.model_validate(photo) if photo else None

    def add_user_photo(
        self, user_id: UUID, photo_data: UserPhotoCreate
    ) -> UserPhotoRead:
        """Adds a new photo, uploading to GCS or saving locally."""

        new_photo = UserPhotos(user_id=user_id, image_url=photo_data.image_url)
        self.db_session.add(new_photo)
        self.db_session.commit()
        self.db_session.refresh(new_photo)
        return UserPhotoRead.model_validate(new_photo)

    def update_user_photo(
        self, user_id: UUID, photo_id: UUID, photo_data: UserPhotoUpdate
    ) -> UserPhotoRead:
        """Updates a user's photo, potentially including re-uploading to storage."""

        photo = self.get_user_photo_by_id(user_id, photo_id)
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        if photo_data.image_url:  # Check if a new image is provided
            # Delete the old image from storage
            if self.environment == "production":
                self._delete_from_gcs(photo.image_url)
            else:
                self._delete_locally(photo.image_url)

            # Upload the new image and update the URL
            filename = f"user_{user_id}/{photo_id}"
            photo.image_url = self._upload_image(filename, photo_data.image_url)

        photo.update(session, **photo_data.model_dump(exclude_unset=True))
        self.db_session.commit()
        self.db_session.refresh(photo)
        return UserPhotoRead.model_validate(photo)

    def delete_user_photo(self, user_id: UUID, photo_id: UUID) -> None:
        """Deletes a user's photo from the database and storage."""

        photo = self.get_user_photo_by_id(user_id, photo_id)
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        if self.environment == "production":
            self._delete_from_gcs(photo.image_url)
        else:
            self._delete_locally(photo.image_url)

        self.db_session.delete(photo)
        self.db_session.commit()

    def _upload_image(self, filename: str, image_data: UploadFile) -> str:
        """Handles image upload based on environment (GCS or local)."""
        if self.environment == "production":
            return self._upload_to_gcs(filename, image_data)
        else:
            return self._save_locally(filename, image_data)

    def _upload_to_gcs(self, filename: str, image_data: UploadFile) -> str:
        """Uploads the image to Google Cloud Storage."""
        bucket = self.storage_client.bucket(self.gcp_bucket_name)
        blob = bucket.blob(filename)

        # Upload from bytes (you'll need to get bytes from the UploadFile)
        image_bytes = image_data.read()
        blob.upload_from_string(image_bytes, content_type=image_data.content_type)
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

    def _delete_from_gcs(self, image_url: str) -> None:
        """Deletes the image from Google Cloud Storage."""
        bucket = self.storage_client.bucket(self.gcp_bucket_name)
        blob = bucket.blob(image_url.split("/")[-1])
        blob.delete()

    def _delete_locally(self, filepath: str) -> None:
        """Deletes the image from the local filesystem."""
        if os.path.exists(filepath):
            os.remove(filepath)
