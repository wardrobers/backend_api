from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from sqlalchemy.orm import Session
from pydantic import UUID4

from ...database.session import get_db
from ...repositories.user.user_photo_repository import UserPhotoRepository
from ...schemas.user.user_photo_schema import (
    UserPhotoCreate,
    UserPhotoRead,
    UserPhotoUpdate,
)

router = APIRouter()


@router.post(
    "/{user_uuid}/photos/",
    response_model=UserPhotoRead,
    status_code=status.HTTP_201_CREATED,
)
def add_user_photo(user_uuid: UUID4, request: Request, file: UploadFile = File(...)):
    """
    Upload a user photo and store its information.
    """
    db: Session = request.state.db
    # Assuming a function to upload the file and return a storage URL
    storage_url = upload_file_to_storage(file)
    photo_data = {"user_uuid": user_uuid, "storage_url": storage_url}
    photo = UserPhotoRepository(db).add_photo(photo_data)
    return photo


@router.get("/{user_uuid}/photos/", response_model=list[UserPhotoRead])
def get_user_photos(user_uuid: UUID4, request: Request):
    """
    Retrieve all photos for a given user.
    """
    db: Session = request.state.db
    photos = UserPhotoRepository(db).get_photos_by_user_uuid(user_uuid)
    return photos


@router.put("/{user_uuid}/photos", response_model=UserPhotoRead)
def update_user_photo(
    photo_uuid: UUID4, photo_update: UserPhotoUpdate, request: Request
):
    """
    Update user photo information.
    """
    db: Session = request.state.db
    updated_photo = UserPhotoRepository(db).update_photo(
        photo_uuid, photo_update.dict(exclude_unset=True)
    )
    if not updated_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return updated_photo


@router.delete("/{user_uuid}/photos", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_photo(photo_uuid: UUID4, request: Request):
    """
    Delete a user photo.
    """
    db: Session = request.state.db
    UserPhotoRepository(db).delete_photo(photo_uuid)
    return {"detail": "Photo deleted successfully"}


def upload_file_to_storage(file: UploadFile) -> str:
    """
    Dummy function to simulate file upload. Implement your actual storage logic here.
    """
    # Logic to save the file to a cloud storage or local storage and return the URL
    return "http://example.com/path/to/photo"
