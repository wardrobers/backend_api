from sqlalchemy import (
    Column,
    String,
    Boolean,
    TIMESTAMP,
    Integer,
    DECIMAL,
    ForeignKey,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()


# SQLAlchemy models
class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    is_notificated = Column(Boolean)
    user_info = relationship("UserInfo", back_populates="user", uselist=False)
    bookings = relationship("Booking", backref="user")


class UserInfo(Base):
    __tablename__ = "user_info"
    __table_args__ = {"extend_existing": True}
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey("users.uuid"))
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    phone_number = Column(String)  # Added new field
    marketing_consent = Column(Boolean)  # Added new field
    user = relationship("User", back_populates="user_info")


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
