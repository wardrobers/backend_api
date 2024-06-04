from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field

from app.schemas.subscriptions import SubscriptionRead
from app.schemas.users.activity.user_activity_schema import UserActivityRead
from app.schemas.users.activity.user_basket_schema import UserBasketRead
from app.schemas.users.activity.user_reviews_and_ratings_schema import (
    UserReviewRatingRead,
)
from app.schemas.users.activity.user_saved_items_schema import UserSavedItemRead
from app.schemas.users.core.data_privacy_consents_schema import DataPrivacyConsentRead
from app.schemas.users.core.user_info_schema import UserInfoRead
from app.schemas.users.profile.user_addresses_schema import UserAddressRead
from app.schemas.users.profile.user_photos_schema import UserPhotoRead
from app.schemas.users.roles.roles_schema import RoleRead


# Basic User Schemas
class UsersBase(BaseModel):
    login: str


class UsersCreate(UsersBase):
    password: str = Field(..., min_length=8, example="StrongP@$$w0rd")
    password_confirmation: str = Field(..., example="StrongP@$$w0rd")


class UsersRead(UsersBase):
    id: UUID4
    info: Optional["UserInfoRead"] = None
    activity: Optional["UserActivityRead"] = None
    basket: Optional["UserBasketRead"] = None
    photos: Optional[list["UserPhotoRead"]] = None
    roles: Optional[list["RoleRead"]] = None
    # orders: Optional[list["OrderRead"]] = None
    subscriptions: Optional[list["SubscriptionRead"]] = None
    reviews_and_ratings: Optional[list["UserReviewRatingRead"]] = None
    saved_items: Optional[list["UserSavedItemRead"]] = None
    # promotions: Optional[list["UserPromotionRead"]] = None
    addresses: Optional[list["UserAddressRead"]] = None
    data_privacy_consents: Optional[list["DataPrivacyConsentRead"]] = None
    # transactions: Optional[list["TransactionRead"]] = None


class UsersUpdate(UsersBase):
    login: Optional[str] = None
    is_notificated: Optional[bool] = None


class UsersDelete(BaseModel):
    id: UUID4


UsersRead.model_rebuild()


# --- User Login Schema ---
class UserLogin(BaseModel):
    login: str
    password: str


# --- Password Reset Request Schema ---
class PasswordResetRequest(BaseModel):
    email: EmailStr


# --- Password Reset Confirmation Schema ---
class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, example="StrongNewP@$$w0rd")


# --- Password Change Schema ---
class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, example="StrongNewP@$$w0rd")
