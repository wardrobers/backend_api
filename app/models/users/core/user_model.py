from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import relationship

from app.models.common import (
    Base,
    BaseMixin,
    SearchMixin,
    CachingMixin,
    BulkActionsMixin,
)

# Import models that are directly related and need explicit import for relationships
from app.models.users import (
    UserInfo,
    UserActivity,
    UserAddresses,
    UserBasket,
    UserSavedItems,
    UserRoles,
    UserReviewsAndRatings,
)
from app.models.subscriptions import Subscriptions
from app.models.promotions import UserPromotions


class User(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "users"

    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, default=False)
    last_login_at = Column(DateTime)

    # Relationships
    info = relationship("UserInfo", uselist=False, backref="users")
    activity = relationship("UserActivity", uselist=False, backref="users")
    basket = relationship("UserBasket", uselist=False, backref="users")
    photos = relationship("UsersPhotos", backref="users")
    role = relationship("Roles", secondary="user_roles", backref="users")
    order = relationship("Order", backref="users")
    subscriptions = relationship("Subscriptions", backref="users")
    reviews_and_ratings = relationship("UserReviewsAndRatings", backref="users")
    saved_items = relationship("UserSavedItems", backref="users")
    promotions = relationship("UserPromotions", backref="users")
    addresses = relationship("UserAddresses", backref="users")
    categories_for_user = relationship("CategoriesForUser", backref="users")
    data_privacy_consents = relationship("DataPrivacyConsents", backref="users")
    transactions = relationship("Transactions", backref="users")
