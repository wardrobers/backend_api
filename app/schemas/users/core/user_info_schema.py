from enum import Enum

from pydantic import UUID4, BaseModel, EmailStr


class UpdateContext(str, Enum):
    CONTACT_DETAILS = "contact_details"
    FULL_PROFILE = "full_profile"
    LENDER_STATUS = "lender_status"


class UserInfoBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr
    lender: bool


class UserInfoCreate(UserInfoBase):
    pass


class UserInfoUpdate(UserInfoBase):
    pass


class UserInfoRead(UserInfoBase):
    id: UUID4
    user_id: UUID4
