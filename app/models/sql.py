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
        "UserSubscription", back_populates="user", uselist=False
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


class UserSubscription(Base):
    __tablename__ = "user_subscription"
    __table_args__ = {"extend_existing": True}
    uuid = Column(
        UUID, primary_key=True, server_default="uuid_generate_v4()", nullable=False
    )
    user_uuid = Column(UUID, nullable=False)
    subscription_type_uuid = Column(UUID, nullable=False)
    subscription_start = Column(DateTime)
    subscription_finish = Column(DateTime)
    count_free_orders = Column(Integer)
    count_orders_available_by_subscription = Column(Integer)
    count_orders_closed_by_subscription = Column(Integer)
    purchase_url = Column(String)
    created_at = Column(DateTime, server_default="now()", nullable=False)
    updated_at = Column(DateTime)
    user = relationship("User", back_populates="user_subscription")
    subscriptions = relationship("Subscriptions", back_populates="user_subscription")


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


class Subscriptions(Base):
    __tablename__ = "user_subscription"
    __table_args__ = {"extend_existing": True}
    uuid = Column(
        UUID, primary_key=True, server_default="uuid_generate_v4()", nullable=False
    )
    perid = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    count_free_orders = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default="now()", nullable=False)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user_subscription = relationship(
        "UserSubscription", back_populates="subscriptions", uselist=False
    )


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {"extend_existing": True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"))
    booking_date = Column(TIMESTAMP)
    status = Column(String)
    payment_method = Column(String)
    price = Column(DECIMAL)
    discount_codes = Column(Text)
    start_date = Column(TIMESTAMP)
    end_date = Column(TIMESTAMP)


class BookingModel(Base):
    __tablename__ = "bookings"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"))
    clothe_uuid = Column(Integer, ForeignKey("clothes.id"))
    start_date = Column(TIMESTAMP)
    end_date = Column(TIMESTAMP)


class ClothesModel(Base):
    __tablename__ = "clothes"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    size = Column(String)
    color = Column(String)
    brand = Column(String)


class ReviewModel(Base):
    __tablename__ = "reviews"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    clothe_uuid = Column(Integer, ForeignKey("clothes.id"))
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"))
    rating = Column(Integer)
    comment = Column(String)


# Add any other SQLAlchemy models as needed
