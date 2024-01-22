import datetime
from typing import List, Optional
from uuid import UUID as PyUUID

from pydantic import BaseModel, Field


class UserInformation(BaseModel):
    name: str
    surname: Optional[str]
    second_name: Optional[str]
    email: str


class UserGet(BaseModel):
    uuid: str
    login: str
    super_admin: bool
    is_notificated: bool
    last_login_at: Optional[str]
    marketing_consent: bool
    created_at: str
    updated_at: Optional[str]
    deleted_at: Optional[str]
    user_info: Optional[UserInformation]
    user_activity: Optional[dict]
    user_subscription: Optional[dict]
    users_photos: Optional[dict]


class UserList(BaseModel):
    users: List[UserGet]


class UserCreate(BaseModel):
    uuid: str
    login: str
    super_admin: bool
    is_notificated: bool
    last_login_at: Optional[str]
    marketing_consent: bool
    created_at: str
    updated_at: Optional[str]
    deleted_at: Optional[str]
    user_info: Optional[UserInformation]
    user_activity: Optional[dict]
    user_subscription: Optional[dict]
    users_photos: Optional[dict]


class UserUpdate(BaseModel):
    uuid: str
    login: str
    super_admin: bool
    is_notificated: bool
    last_login_at: Optional[str]
    marketing_consent: bool
    created_at: str
    updated_at: Optional[str]
    deleted_at: Optional[str]
    user_info: Optional[UserInformation]
    user_activity: Optional[dict]
    user_subscription: Optional[dict]
    users_photos: Optional[dict]


class UserDelete(BaseModel):
    uuid: str


class UserLogin(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ClothesBase(BaseModel):
    name: str
    size: str
    color: str
    brand: str


class ClothesCreate(ClothesBase):
    pass


class Clothes(ClothesBase):
    id: int

    class Config:
        orm_mode = True


class ClothesUpdate(BaseModel):
    name: Optional[str]
    size: Optional[str]
    color: Optional[str]
    brand: Optional[str]


class BookingBase(BaseModel):
    user_uuid: PyUUID
    clothe_uuid: PyUUID
    start_date: datetime.datetime
    end_date: datetime.datetime


class BookingCreate(BookingBase):
    pass


class Booking(BookingBase):
    id: int

    class Config:
        orm_mode = True


class BookingUpdate(BaseModel):
    status: Optional[str]
    payment_method: Optional[str]
    price: Optional[float]
    discount_codes: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]


class ReviewBase(BaseModel):
    clothe_uuid: PyUUID
    user_uuid: PyUUID
    rating: int
    comment: str


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True


class ReviewUpdate(BaseModel):
    rating: Optional[int]
    comment: Optional[str]


class PaginationQuery(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(10, gt=0)


class SortingQuery(BaseModel):
    sort_by: str = Field("id", description="Sort by a field like 'id', 'name', 'brand'")
    order: str = Field(
        "asc", description="'asc' for ascending or 'desc' for descending"
    )


class AdvancedSearchQuery(BaseModel):
    min_price: Optional[float]
    max_price: Optional[float]
    min_rating: Optional[int]
    material: Optional[str]
