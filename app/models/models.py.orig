import datetime
from pydoc import text
from typing import List, Optional
from uuid import UUID as PyUUID

from pydantic import UUID4, BaseModel, Field


# Auth
class UserInformation(BaseModel):
    uuid: Optional[UUID4]
    name: str
    surname: Optional[str]
    second_name: Optional[str]
    email: str


class SubscriptionType(BaseModel):
    uuid: Optional[UUID4]
    name: str
    period_uuid: str
    price: str
    count_free_orders: int
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


class UserSubscriptionType(BaseModel):
    uuid: Optional[UUID4]
    subscription_type_uuid: Optional[SubscriptionType]
    subscription_start: datetime.datetime
    subscription_finish: datetime.datetime
    count_free_orders: int
    count_orders_available_by_subscription: int
    count_orders_closed_by_subscription: int
    purchase_url: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class SubscriptionTypeList(BaseModel):
    subscription_types: List[SubscriptionType]


class SubscriptionTypeDelete(BaseModel):
    uuid: UUID4


class UsersPhotos(BaseModel):
    uuid: Optional[UUID4]
    product_uuid: UUID4
    showcase: bool
    created_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


class UsersPhotosList(BaseModel):
    users_photos: List[UsersPhotos]


class UsersPhotosDelete(BaseModel):
    uuid: UUID4


class UserActivity(BaseModel):
    uuid: Optional[UUID4]
    user_uuid: UUID4
    total_confirmed_orders: int
    total_canceled_orders: int
    activity_orders: int
    subscription_now: bool
    total_money_spent: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class UserActivityList(BaseModel):
    user_activities: List[UserActivity]


class UserActivityDelete(BaseModel):
    uuid: UUID4


class User(BaseModel):
    uuid: Optional[UUID4]
    login: str
    super_admin: bool
    is_notificated: bool
    last_login_at: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]
    user_info: Optional[UserInformation]
    user_activity: Optional[UserActivity]
    user_subscription: Optional[UserSubscriptionType]
    users_photos: Optional[UsersPhotos]


class UserList(BaseModel):
    users: List[User]


class UserDelete(BaseModel):
    uuid: UUID4


class UserLogin(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Product
# Модель для таблицы brands
class Brand(BaseModel):
    uuid: Optional[UUID4]
    name: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


# Модель для таблицы product_types
class ProductType(BaseModel):
    uuid: Optional[UUID4]
    name: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


# Модель для таблицы catalog_product_types
class CatalogProductType(BaseModel):
    uuid: Optional[UUID4]
    product_type_uuid: UUID4
    product_catalog_uuid: UUID4
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    product_type: Optional[ProductType]


class CatalogProductTypeList(BaseModel):
    catalog_product_types: List[CatalogProductType]


# Модель для таблицы categories
class Category(BaseModel):
    uuid: Optional[UUID4]
    product_type_uuid: UUID4
    name: Optional[str]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]
    product_type: Optional[ProductType]


class CategoryList(BaseModel):
    categories: List[Category]


# Модель для таблицы colores
class Color(BaseModel):
    uuid: Optional[UUID4]
    color: Optional[str]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


class Colores(BaseModel):
    colores: List[Color]


# Модель для таблицы Materials
class Material(BaseModel):
    uuid: Optional[UUID4]
    name: str
    product_type_uuid: UUID4
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]
    product_type: Optional[ProductType]


# Модель для таблицы rental_periods


class rentalPeriod(BaseModel):
    uuid: Optional[UUID4]
    name: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


class rentalPeriods(BaseModel):
    rental_periods: List[rentalPeriod]


# Модель для таблицы prices
class Price(BaseModel):
    uuid: Optional[UUID4]
    product_uuid: UUID4
    time_period_uuid: UUID4
    time_value: int
    price: float
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    rental_periods: Optional[rentalPeriod]


# Модель для таблицы product_categories
class ProductCategory(BaseModel):
    uuid: Optional[UUID4]
    product_catalog_uuid: UUID4
    category_uuid: UUID4
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]
    category: Optional[Category]


class ProductCategoryList(BaseModel):
    product_categories: List(ProductCategory)


# Модель для таблицы product_materials
class ProductMaterial(BaseModel):
    product_catalog_uuid: UUID4
    material_uuid: UUID4
    percent: Optional[int]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]
    materials: Optional[Material]


class ProductMaterialList(BaseModel):
    product_materials: List[ProductMaterial]


# Модель для таблицы product_photoes
class ProductPhoto(BaseModel):
    uuid: Optional[UUID4]
    product_uuid: UUID4
    showcase: bool
    created_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


class ProductPhotoes(BaseModel):
    product_photoes: List[ProductPhoto]


class ProductCatalogPhoto(BaseModel):
    uuid: Optional[UUID4]
    product_uuid: UUID4
    created_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


# Модель для таблицы product_status
class ProductStatus(BaseModel):
    uuid: Optional[UUID4]
    code: str
    name: str
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


class ProductsCatalog(BaseModel):
    uuid: Optional[UUID4]
    brand_uuid: UUID4
    name: str
    description: text
    instructions: str
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]
    product_catalog_photo: Optional[ProductCatalogPhoto]
    brand: Optional[Brand]
    product_materials: Optional[ProductMaterialList]
    catalog_product_type: Optional[CatalogProductTypeList]
    product_categories: Optional[ProductCategoryList]


# Модель для таблицы Sizes
class Size(BaseModel):
    uuid: Optional[UUID4]
    back_length: Optional[str]
    sleeve_length: Optional[str]
    leg_length: Optional[str]
    size_EU_code: Optional[str]
    size_UK_code: Optional[str]
    size_US_code: Optional[str]
    size_IT_code: Optional[str]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


# Модель для таблицы products
class Product(BaseModel):
    uuid: Optional[UUID4]
    products_catalog_uuid: UUID4
    status_code: str
    color_uuid: UUID4
    number: str
    name: Optional[str]
    article: Optional[str]
    size_uuid: UUID4
    usage_count: int = 0
    usage_seconds: int = 0
    factory_number: Optional[str]
    base_price: float
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]
    product_catalog: Optional[ProductsCatalog]
    sizes: Optional[Size]
    status: Optional[ProductStatus]
    price: Optional[Price]
    product_status: Optional[ProductStatus]
    color: Optional[Color]
    product_photoes: Optional[ProductPhotoes]


# Booking
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
