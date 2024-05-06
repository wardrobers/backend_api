from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base

# Import models that are directly related and need explicit import for relationships
from .user_info_model import UserInfo
from .user_activity_model import UserActivity
from .user_basket_model import UserBasket
from .user_addresses_model import UserAddresses
from .user_saved_items_model import UserSavedItems
from .subscriptions_model import Subscriptions
from .user_reviews_and_ratings_model import UserReviewsAndRatings
from .user_promotions_model import UserPromotions
from .user_roles_model import UserRoles


class User(Base):
    __tablename__ = "users"

    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, default=False)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)

    # Relationships
    user_info = relationship("UserInfo", uselist=False, backref="users")
    user_activity = relationship("UserActivity", uselist=False, backref="users")
    user_basket = relationship("UserBasket", uselist=False, backref="users")
    user_photos = relationship("UsersPhotos", backref="users")
    role = relationship("Roles", secondary="user_roles", backref="users")
    order = relationship("Order", backref="users")
    subscriptions = relationship("Subscriptions", backref="users")
    user_reviews_and_ratings = relationship("UserReviewsAndRatings", backref="users")
    user_saved_items = relationship("UserSavedItems", backref="users")
    user_promotions = relationship("UserPromotions", backref="users")
    user_addresses = relationship("UserAddresses", backref="users")
    categories_for_user = relationship("CategoriesForUser", backref="users")
