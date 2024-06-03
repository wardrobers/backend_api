from pydantic import UUID4, BaseModel


class UserPhotoBase(BaseModel):
    image_url: str


class UserPhotoCreate(UserPhotoBase):
    pass


class UserPhotoRead(UserPhotoBase):
    iid: UUID4
    user_id: UUID4
