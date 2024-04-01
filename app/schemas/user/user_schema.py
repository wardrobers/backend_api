from pydantic import BaseModel, UUID4, Field
from typing import Optional
from datetime import datetime

from ...schemas.user.user_info_schema import UserInfoBase


class UserBase(BaseModel):
    uuid: UUID4 = Field(default_factory=UUID4)
    login: str
    password: Optional[str] = None
    is_notified: Optional[bool] = False
    marketing_consent: Optional[bool] = False


class UserCreate(BaseModel):
    uuid: UUID4 = Field(default_factory=UUID4)
    login: str
    password: str


class UserRead(BaseModel):
    uuid: UUID4
    login: str
    is_notified: bool
    marketing_consent: bool
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    user_info: Optional[UserInfoBase] = None


class UserUpdate(BaseModel):
    login: Optional[str] = None
    is_notified: Optional[bool] = None
    marketing_consent: Optional[bool] = None
    user_info: Optional[UserInfoBase] = (
        None  # Assume nested updates are handled appropriately.
    )


class UserDelete(BaseModel):
    uuid: UUID4
