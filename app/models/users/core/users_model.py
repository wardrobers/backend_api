from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base
from app.models.orders.core.orders_model import Orders
from app.models.orders.payments.transactions_model import Transactions
from app.models.subscriptions.subscriptions_model import Subscriptions
from app.models.users.activity.user_activity_model import UserActivity
from app.models.users.activity.user_basket_model import UserBasket
from app.models.users.activity.user_reviews_and_ratings_model import (
    UserReviewsAndRatings,
)
from app.models.users.activity.user_saved_items_model import UserSavedItems
from app.models.users.core.data_privacy_consents_model import DataPrivacyConsents
from app.models.users.core.user_info_model import UserInfo
from app.models.users.profile.user_photos_model import UserPhotos


class Users(Base):
    __tablename__ = "users"

    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, default=False)
    last_login_at = Column(DateTime)

    # Relationships
    info = relationship(
        "UserInfo", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    activity = relationship(
        "UserActivity",
        uselist=False,
        backref="users",
        cascade="all, delete-orphan",
    )
    basket = relationship(
        "UserBasket",
        backref="users",
        cascade="all, delete-orphan",
    )
    photos = relationship("UserPhotos", backref="users", cascade="all, delete-orphan")
    user_roles = relationship(
        "UserRoles",
        backref="users",
        cascade="all, delete-orphan",
    )
    orders = relationship(
        "Orders",
        backref="users",
        cascade="all, delete-orphan",
    )
    subscriptions = relationship(
        "Subscriptions", backref="users", cascade="all, delete-orphan"
    )
    reviews_and_ratings = relationship(
        "UserReviewsAndRatings",
        backref="users",
        cascade="all, delete-orphan",
    )
    saved_items = relationship(
        "UserSavedItems", backref="users", cascade="all, delete-orphan"
    )
    promotions = relationship(
        "UserPromotions", backref="users", cascade="all, delete-orphan"
    )
    addresses = relationship(
        "UserAddresses", backref="users", cascade="all, delete-orphan"
    )
    data_privacy_consents = relationship(
        "DataPrivacyConsents",
        uselist=False,
        backref="users",
        cascade="all, delete-orphan",
    )
    transactions = relationship("Transactions", backref="users")
