# app/routers/users/profile/user_photos_router.py
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_async_session
from app.models.users import Users
from app.repositories.users import UserPhotosRepository
from app.schemas.common import Message
from app.schemas.users import UserPhotoRead
from app.services.users import AuthService, UserPhotosService

router = APIRouter()


# Dependency to get user photos service
async def get_user_photos_service(
    db_session: AsyncSession = Depends(get_async_session),
):
    user_photo_repository = UserPhotosRepository(db_session)
    return UserPhotosService(user_photo_repository)


@router.get("/", response_model=list[UserPhotoRead], response_model=Message)
async def get_user_photos(
    current_user: Users = Depends(AuthService.get_current_user),
    user_photos_service: UserPhotosService = Depends(get_user_photos_service),
):
    """
    Retrieves all photos associated with the currently authenticated user.

    **Requires Authentication (JWT).**

    **Response (Success - 200 OK):**
        - `List[UserPhotoRead]` (schema): A list of user photos.
    """
    return await user_photos_service.get_user_photos(current_user.id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPhotoRead)
async def upload_user_photo(
    photo: UploadFile = File(...),
    current_user: Users = Depends(AuthService.get_current_user),
    user_photos_service: UserPhotosService = Depends(get_user_photos_service),
):
    """
    Uploads a new photo for the currently authenticated user.

    **Requires Authentication (JWT).**

    **Request Body:**
        - `photo` (UploadFile): The image file to upload (JPEG or PNG).

    **Response (Success - 201 Created):**
        - `UserPhotoRead` (schema): The newly added user photo object.

    **Error Codes:**
        - 400 Bad Request: If the provided photo data is invalid (e.g., wrong file type).
    """
    return await user_photos_service.add_user_photo(current_user.id, photo)


@router.delete(
    "/{photo_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=Message
)
async def delete_user_photo(
    photo_id: UUID,
    current_user: Users = Depends(AuthService.get_current_user),
    user_photos_service: UserPhotosService = Depends(get_user_photos_service),
):
    """
    Deletes a photo associated with the current user.

    **Requires Authentication (JWT).**

    **Response (Success - 204 No Content):**
        - Indicates successful deletion.

    **Error Codes:**
        - 403 Forbidden: If the user is not authorized to delete the photo.
        - 404 Not Found: If the photo with the provided ID is not found for the user.
    """
    await user_photos_service.delete_user_photo(current_user.id, photo_id)
