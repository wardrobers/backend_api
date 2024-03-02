from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from pydantic import UUID4

from ..dependencies import get_db
from ..repositories.user_photo_repository import UserPhotoRepository
from ..schemas.user_photo_schema import UserPhotoCreate, UserPhotoRead, UserPhotoUpdate

router = APIRouter()

@router.post("/users/{user_uuid}/photos/", response_model=UserPhotoRead, status_code=status.HTTP_201_CREATED)
def add_user_photo(user_uuid: UUID4, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a user photo and store its information.
    """
    # Assuming a function to upload the file and return a storage URL
    storage_url = upload_file_to_storage(file)
    photo_data = {"user_uuid": user_uuid, "storage_url": storage_url}
    photo = UserPhotoRepository(db).add_photo(photo_data)
    return photo

@router.get("/users/{user_uuid}/photos/", response_model=list[UserPhotoRead])
def get_user_photos(user_uuid: UUID4, db: Session = Depends(get_db)):
    """
    Retrieve all photos for a given user.
    """
    photos = UserPhotoRepository(db).get_photos_by_user_uuid(user_uuid)
    return photos

@router.put("/users/{photo_uuid}/photos", response_model=UserPhotoRead)
def update_user_photo(photo_uuid: UUID4, photo_update: UserPhotoUpdate, db: Session = Depends(get_db)):
    """
    Update user photo information.
    """
    updated_photo = UserPhotoRepository(db).update_photo(photo_uuid, photo_update.dict(exclude_unset=True))
    if not updated_photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return updated_photo

@router.delete("/users/{photo_uuid}/photos", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_photo(photo_uuid: UUID4, db: Session = Depends(get_db)):
    """
    Delete a user photo.
    """
    UserPhotoRepository(db).delete_photo(photo_uuid)
    return {"detail": "Photo deleted successfully"}

def upload_file_to_storage(file: UploadFile) -> str:
    """
    Dummy function to simulate file upload. Implement your actual storage logic here.
    """
    # Logic to save the file to a cloud storage or local storage and return the URL
    return "http://example.com/path/to/photo"
