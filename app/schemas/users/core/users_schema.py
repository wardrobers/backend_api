from typing import Optional

from pydantic import UUID4, BaseModel, Field


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
    orders: Optional[list["OrderRead"]] = None
    subscriptions: Optional[list["SubscriptionRead"]] = None
    reviews_and_ratings: Optional[list["UserReviewRatingRead"]] = None
    saved_items: Optional[list["UserSavedItemRead"]] = None
    promotions: Optional[list["UserPromotionRead"]] = None
    addresses: Optional[list["UserAddressRead"]] = None
    categories_for_user: Optional[list["CategoryForUserRead"]] = None
    data_privacy_consents: Optional[list["DataPrivacyConsentRead"]] = None
    transactions: Optional[list["TransactionRead"]] = None


class UsersUpdate(UsersBase):
    login: Optional[str] = None
    is_notificated: Optional[bool] = None


class UsersDelete(BaseModel):
    id: UUID4


UsersRead.model_rebuild()
