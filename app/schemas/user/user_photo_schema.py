from pydantic import BaseModel, UUID4, HttpUrl
from datetime import datetime


class UserPhotoBase(BaseModel):
    storage_url: HttpUrl


class UserPhotoCreate(UserPhotoBase):
    pass


class UserPhotoRead(UserPhotoBase):
    uuid: UUID4
    user_uuid: UUID4
    created_at: datetime
    deleted_at: datetime | None

    class Config:
        from_attributes = True


class UserPhotoUpdate(BaseModel):
    storage_url: HttpUrl | None
