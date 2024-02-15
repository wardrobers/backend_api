from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime


class UserPhotoBase(BaseModel):
    uuid: Optional[UUID4]
    product_uuid: UUID4
    showcase: bool
    created_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


class UserPhotoList(BaseModel):
    users_photos: list[UsersPhotos]


class UserPhotoDelete(BaseModel):
    uuid: UUID4