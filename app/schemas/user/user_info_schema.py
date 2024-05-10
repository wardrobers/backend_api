from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime


class UserInfoBase(BaseModel):
    name: str
    surname: Optional[str] = None
    second_name: Optional[str] = None
    email: EmailStr

    class Config:
        from_attributes = True


class UserInfoCreate(UserInfoBase):
    # Assuming user_id is provided externally, not through the client directly
    pass


class UserInfoRead(UserInfoBase):
    uuid: UUID4
    user_id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class UserInfoUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    second_name: Optional[str] = None
    email: Optional[EmailStr] = None
