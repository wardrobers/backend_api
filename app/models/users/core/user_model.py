from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base

# Import models that are directly related and need explicit import for relationships
from .user_info_model import UserInfo
from ..activity.user_activity_model import UserActivity
from ..profile.user_basket_model import UserBasket
from ..profile.user_addresses_model import UserAddresses
from ..activity.user_saved_items_model import UserSavedItems
from ...subscriptions.subscriptions_model import Subscriptions
from ..activity.user_reviews_and_ratings_model import UserReviewsAndRatings
from ...promotions.user_promotions_model import UserPromotions
from ..roles.user_roles_model import UserRoles


class User(Base):
    __tablename__ = "users"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, default=False)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

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
