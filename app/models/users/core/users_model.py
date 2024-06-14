from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base
from app.models.users.activity.user_activity_model import UserActivity
from app.models.users.activity.user_basket_model import UserBasket
from app.models.users.core.user_info_model import UserInfo
from app.models.users.profile.user_photos_model import UserPhotos
from app.models.users.activity.user_reviews_and_ratings_model import UserReviewsAndRatings
from app.models.users.activity.user_saved_items_model import UserSavedItems
from app.models.subscriptions.subscriptions_model import Subscriptions
from app.models.orders.core.orders_model import Orders
from app.models.users.core.data_privacy_consents_model import DataPrivacyConsents
from app.models.orders.payments.transactions_model import Transactions


class Users(Base):
    __tablename__ = "users"

    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, default=False)
    last_login_at = Column(DateTime)

    # Relationships
    info = relationship("UserInfo", uselist=False, backref="users")
    activity = relationship(
        "UserActivity",
        uselist=False,
        backref="users",
    )
    basket = relationship(
        "UserBasket",
        uselist=False,
        backref="users",
    )
    photos = relationship("UserPhotos", backref="users")
    user_roles = relationship(
        "UserRoles",
        backref="users",
    )
    orders = relationship("Orders", backref="users")
    subscriptions = relationship(
        "Subscriptions", backref="users"
    )
    reviews_and_ratings = relationship(
        "UserReviewsAndRatings",
        backref="users",
    )
    saved_items = relationship(
        "UserSavedItems",
        backref="users",
    )
    promotions = relationship("UserPromotions", backref="users")
    addresses = relationship("UserAddresses", backref="users")
    data_privacy_consents = relationship(
        "DataPrivacyConsents",
        backref="users",
    )
    transactions = relationship("Transactions", backref="users")
