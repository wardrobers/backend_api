from pydantic import UUID4, BaseModel
from typing import Optional

class UserPhotoBase(BaseModel):
    image_url: str


class UserPhotoCreate(UserPhotoBase):
    pass


class UserPhotoRead(UserPhotoBase):
    id: UUID4
    user_id: UUID4


class UserPhotoUpdate(BaseModel):
    image_url: Optional[str] = None