from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID as PyUUID
import datetime


class UserInformation(BaseModel):
    name: str
    surname: str
    email: str
    phone_number: str
    marketing_consent: bool


class UserCreate(BaseModel):
    login: str
    password: str
    is_notificated: bool
    user_info: UserInformation


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
