from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID

from app.models.users import User, UserPhotos
from app.database import get_async_session
from app.routers.users import auth_handler


router = APIRouter()


@router.post("/photos", status_code=status.HTTP_201_CREATED)
async def upload_user_photo(
    photo_data,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Uploads a new photo and associates it with the current user's profile.

    Requires Authentication (JWT).

    Request Body:
        - storage_url (str): URL where the uploaded photo is stored.

    Response (Success - 201 Created):
        - UserPhotoRead (schema): A JSON representation of the newly added photo object.

    Error Codes:
        - 400 Bad Request: If the provided photo data is invalid.
    """
    new_photo = UserPhotos(user_id=current_user.id, storage_url=photo_data.storage_url)
    db_session.add(new_photo)
    await db_session.commit()
    await db_session.refresh(new_photo)
    return new_photo


@router.get("/photos")
async def get_user_photos(
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Retrieves all photos associated with the currently authenticated user.

    Requires Authentication (JWT).

    Response (Success - 200 OK):
        - list[UserPhotoRead]: A JSON array of user photo objects.
    """
    return current_user.photos


@router.put("/photos")
async def update_user_photo(
    photo_id: UUID,
    photo_update,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Updates a specific photo belonging to the currently authenticated user.

    Requires Authentication (JWT).

    Request Body:
        - storage_url (str): The updated URL for the photo.

    Response (Success - 200 OK):
        - UserPhotoRead (schema): A JSON representation of the updated photo object.

    Error Codes:
        - 404 Not Found: If no photo with the provided photo_id is found for the user.
    """
    photo = next((p for p in current_user.photos if p.id == photo_id), None)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    update_data = photo_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(photo, key, value)

    await db_session.commit()
    await db_session.refresh(photo)
    return photo


@router.delete("/photos", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_photo(
    photo_id: UUID,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(auth_handler.get_current_user),
):
    """
    Soft deletes a photo associated with the current user.

    Requires Authentication (JWT).

    Response (Success - 204 No Content): Indicates successful deletion.

    Error Codes:
        - 404 Not Found: If no photo with the provided photo_id is found for the user.
    """
    photo = next((p for p in current_user.photos if p.id == photo_id), None)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    await photo.soft_delete(db_session)
