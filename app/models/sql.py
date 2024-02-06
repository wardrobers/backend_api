import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import NUMERICTYPE, DateTime, Numeric

from app.models.sql import (
    DECIMAL,
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)

Base = declarative_base()


# SQLAlchemy models
# Auth


class SubscriptionPeriod(Base):
    __tablename__ = "subscription_periods"

    uuid = Column(
        UUID(as_uuid=True), primary_key=True, server_default="uuid_generate_v4()"
    )
    name = Column(String)
    created_at = Column(DateTime, nullable=False, server_default="now()")
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class SubscriptionType(Base):
    __tablename__ = "subscription_types"
    __table_args__ = {"extend_existing": True}
    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default="uuid_generate_v4()",
        nullable=False,
    )
    name = Column(String)
    period_uuid = Column(
        UUID(as_uuid=True), ForeignKey("subscription_periods.uuid"), nullable=False
    )
    price = Column(Numeric, nullable=False)
    count_free_orders = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default="now()")
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    subscription_periods = relationship(
        "SubscriptionPeriod", back_populates="subscriptions", uselist=False
    )


class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = {"extend_existing": True}
    uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default="uuid_generate_v4()",
        nullable=False,
    )
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False)
    subscription_type_uuid = Column(
        UUID(as_uuid=True), ForeignKey("subscription_types.uuid"), nullable=False
    )
    subscription_start = Column(DateTime)
    subscription_finish = Column(DateTime)
    count_free_orders = Column(Integer)
    count_orders_available_by_subscription = Column(Integer)
    count_orders_closed_by_subscription = Column(Integer)
    purchase_url = Column(String)
    created_at = Column(
        DateTime, nullable=False, server_default="now()", nullable=False
    )
    updated_at = Column(DateTime)

    users = relationship("User", back_populates="user_subscription")
    subscription_types = relationship(
        "SubscriptionType", back_populates="user_subscription"
    )


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    uuid = Column(
        UUID, primary_key=True, server_default="uuid_generate_v4()", nullable=False
    )
    login = Column(String, nullable=False)
    super_admin = Column(Boolean)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, nullable=False, default=False)
    last_login_at = Column(DateTime)
    marketing_consent = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, server_default="now()", nullable=False)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user_info = relationship("UserInfo", back_populates="user", uselist=False)
    user_activity = relationship("UserActivity", back_populates="user", uselist=False)
    user_subscription = relationship(
        "Subscription", back_populates="user", uselist=False
    )
    users_photos = relationship("UsersPhotos", back_populates="user", uselist=False)
    bookings = relationship("Booking", backref="user")


class UserInfo(Base):
    __tablename__ = "user_info"
    __table_args__ = {"extend_existing": True}
    uuid = Column(
        UUID, primary_key=True, server_default="uuid_generate_v4()", nullable=False
    )
    user_uuid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String)
    second_name = Column(String)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, server_default="now()", nullable=False)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user = relationship("User", back_populates="user_info")


class UserActivity(Base):
    __tablename__ = "user_activity"
    __table_args__ = {"extend_existing": True}
    uuid = Column(
        UUID, primary_key=True, server_default="uuid_generate_v4()", nullable=False
    )
    user_uuid = Column(UUID, nullable=False)
    total_confirmed_orders = Column(Integer, nullable=False, default=0)
    total_canceled_orders = Column(Integer, nullable=False, default=0)
    activity_orders = Column(Integer, nullable=False, default=0)
    subscription_now = Column(Boolean, nullable=False, default=False)
    total_money_spent = Column(NUMERICTYPE)
    created_at = Column(DateTime, server_default="now()", nullable=False)
    updated_at = Column(DateTime)
    user = relationship("User", back_populates="user_activity")


class UsersPhotos(Base):
    __tablename__ = "user_subscription"
    __table_args__ = {"extend_existing": True}
    uuid = Column(
        UUID, primary_key=True, server_default="uuid_generate_v4()", nullable=False
    )
    user_uuid = Column(UUID, nullable=False)
    storage_url = Column(String, nullable=False)
    created_at = Column(DateTime, server_default="now()", nullable=False)
    deleted_at = Column(DateTime)
    user = relationship("User", back_populates="users_photos")


# Products
class Brand(Base):
    __tablename__ = "brands"

    uuid = Column("uuid", String, primary_key=True, default="uuid_generate_v4()")
    name = Column("name", String, nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default="now()")
    updated_at = Column("updated_at", DateTime)
    deleted_at = Column("deleted_at", DateTime)


class CatalogProductType(Base):
    __tablename__ = "catalog_product_types"

    uuid = Column("uuid", String, primary_key=True, default="uuid_generate_v4()")
    product_type_uuid = Column("product_type_uuid", String, nullable=False)
    product_catalog_uuid = Column("product_catalog_uuid", String, nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default="now()")
    deleted_at = Column("deleted_at", DateTime)


class Category(Base):
    __tablename__ = "categories"

    uuid = Column("uuid", String, primary_key=True, default="uuid_generate_v4()")
    product_type_uuid = Column("product_type_uuid", String, nullable=False)
    name = Column("name", String)
    created_at = Column("created_at", DateTime, default="now()")
    updated_at = Column("updated_at", DateTime)
    deleted_at = Column("deleted_at", DateTime)


class Color(Base):
    __tablename__ = "colores"

    uuid = Column("uuid", String, primary_key=True, default="uuid_generate_v4()")
    color = Column("color", String)
    created_at = Column("created_at", DateTime, nullable=False, default="now()")
    updated_at = Column("updated_at", DateTime)
    deleted_at = Column("deleted_at", DateTime)


class Material(Base):
    __tablename__ = "Materials"

    uuid = Column("uuid", String, primary_key=True, default="uuid_generate_v4()")
    name = Column("name", String)
    product_type_uuid = Column("product_type_uuid", String, nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default="now()")
    updated_at = Column("updated_at", DateTime)
    deleted_at = Column("deleted_at", DateTime)


class Price(Base):
    __tablename__ = "prices"

    uuid = Column("uuid", String, primary_key=True, default="uuid_generate_v4()")
    product_uuid = Column("product_uuid", String, nullable=False)
    time_period_uuid = Column("time_period_uuid", String, nullable=False)
    time_value = Column("time_value", Integer, nullable=False)
    price = Column("price", Numeric, nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default="now()")
    updated_at = Column("updated_at", DateTime)


class ProductCategory(Base):
    __tablename__ = "product_categories"

    uuid = Column("uuid", String, primary_key=True, default="uuid_generate_v4()")
    product_catalog_uuid = Column("product_catalog_uuid", String, nullable=False)
    category_uuid = Column("category_uuid", String, nullable=False)
    created_at = Column("created_at", DateTime, nullable=False, default="now()")
    deleted_at = Column("deleted_at", DateTime)


class ProductMaterial(Base):
    __tablename__ = "product_materials"

    product_catalog_uuid = Column("product_catalog_uuid", String, nullable=False)
    material_uuid = Column("material_uuid", String, nullable=False)
    percent = Column("percent", Integer)
    created_at = Column("created_at", DateTime, nullable=False, default="now()")
    updated_at = Column("updated_at", DateTime)
    deleted_at = Column("deleted_at", DateTime)


class ProductPhoto(Base):
    __tablename__ = "product_photoes"

    uuid = Column("uuid", String, primary_key=True, default="uuid_generate_v4()")
    product_uuid = Column("product_uuid", String, nullable=False)
    showcase = Column("showcase", Boolean, nullable=False, default=False)
    created_at = Column("created_at", DateTime, default="now()")
    deleted_at = Column("deleted_at", DateTime)


class ProductStatus(Base):
    __tablename__ = "product_status"

    uuid = Column(UUID(), primary_key=True)
    code = Column(String(), nullable=False)
    name = Column(String(), nullable=False)
    created_at = Column(DateTime(), nullable=False, server_default="now()")
    updated_at = Column(DateTime())
    deleted_at = Column(DateTime())


class ProductTypes(Base):
    __tablename__ = "product_types"

    uuid = Column(UUID(), primary_key=True)
    name = Column(String(), nullable=False)
    created_at = Column(DateTime(), nullable=False, server_default="now()")
    updated_at = Column(DateTime())
    deleted_at = Column(DateTime())


class Products(Base):
    __tablename__ = "products"

    uuid = Column(UUID(), primary_key=True)
    status_code = Column(String(), ForeignKey("product_status.code"), nullable=False)
    color_uuid = Column(UUID(), nullable=False)
    number = Column(String(), nullable=False)
    name = Column(String())
    article = Column(String())
    size_uuid = Column(UUID(), ForeignKey("sizies.uuid"), nullable=False)
    usage_count = Column(Integer(), nullable=False, default=0)
    usage_seconds = Column(int(), nullable=False, default=0)
    factory_number = Column(String())
    base_price = Column(Numeric(), nullable=False)
    created_at = Column(DateTime(), nullable=False, server_default="now()")
    updated_at = Column(DateTime())
    deleted_at = Column(DateTime())

    status = relationship("ProductStatus", foreign_keys=[status_code])
    size = relationship("Sizies", foreign_keys=[size_uuid])


class ProductsCatalog(Base):
    __tablename__ = "products_catalog"

    uuid = Column(UUID(), primary_key=True)
    brand_uuid = Column(UUID(), nullable=False)
    name = Column(String())
    description = Column(Text())
    instructions = Column(Text())
    created_at = Column(DateTime(), nullable=False, server_default="now()")
    updated_at = Column(DateTime())
    deleted_at = Column(DateTime())

    brand = relationship("Brands", foreign_keys=[brand_uuid])


class ProductsCatalogPhotoes(Base):
    __tablename__ = "products_catalog_photoes"

    uuid = Column(UUID(), primary_key=True)
    products_catalog_uuid = Column(
        UUID(), ForeignKey("products_catalog.uuid"), nullable=False
    )
    product_uuid = Column(UUID(), ForeignKey("products.uuid"), nullable=False)
    showcase = Column(Boolean(), nullable=False, default=False)
    created_at = Column(DateTime(), server_default="now()")
    deleted_at = Column(DateTime())

    catalog = relationship("ProductsCatalog", foreign_keys=[products_catalog_uuid])


class RentalPeriods(Base):
    __tablename__ = "rental_periods"

    uuid = Column(UUID(), primary_key=True)
    name = Column(String())
    created_at = Column(DateTime(), nullable=False, server_default="now()")
    updated_at = Column(DateTime())
    deleted_at = Column(DateTime())


class Sizies(Base):
    __tablename__ = "sizies"

    uuid = Column(UUID(), primary_key=True)
    back_length = Column(Numeric())
    sleeve_length = Column(Numeric())
    leg_length = Column(Numeric())
    size_EU_code = Column(String())
    size_UK_code = Column(String())
    size_US_code = Column(String())
    size_IT_code = Column(String())
    created_at = Column(DateTime(), nullable=False, server_default="now()")
    updated_at = Column(DateTime())
    deleted_at = Column(DateTime())


class ProductPhotoes(Base):
    __tablename__ = "product_photoes"

    uuid = Column(UUID(), primary_key=True)
    product_uuid = Column(UUID(), ForeignKey("products.uuid"))

    product = relationship("Products", foreign_keys=[product_uuid])


class ProductCategories(Base):
    __tablename__ = "product_categories"

    uuid = Column(UUID(), primary_key=True)
    category_uuid = Column(UUID(), ForeignKey("categories.uuid"))
    category = relationship("Categories", foreign_keys=[category_uuid])


class Prices(Base):
    __tablename__ = "prices"

    uuid = Column(UUID(), primary_key=True)
    product_uuid = Column(UUID(), ForeignKey("products.uuid"))
    time_period_uuid = Column(UUID(), ForeignKey("rental_periods.uuid"))

    product = relationship("Products", foreign_keys=[product_uuid])
    time_period = relationship("RentalPeriods", foreign_keys=[time_period_uuid])


class ProductMaterials(Base):
    __tablename__ = "product_materials"

    uuid = Column(UUID(), primary_key=True)
    product_catalog_uuid = Column(UUID(), ForeignKey("products_catalog.uuid"))
    material_uuid = Column(UUID(), ForeignKey("materials.uuid"))

    catalog = relationship("ProductsCatalog", foreign_keys=[product_catalog_uuid])


# Booking


# Add any other SQLAlchemy models as needed
