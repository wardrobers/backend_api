from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Users(Base):
    __tablename__ = "users"

    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_notificated = Column(Boolean, default=False)
    last_login_at = Column(DateTime)

    # Relationships
    info = relationship(
        "app.models.users.core.user_info_model.UserInfo", uselist=False, backref="users"
    )
    activity = relationship(
        "app.models.users.UserActivity",
        uselist=False,
        backref="users",
    )
    basket = relationship(
        "app.models.users.UserBasket",
        uselist=False,
        backref="users",
    )
    photos = relationship(
        "app.models.users.UserPhotos", backref="users"
    )
    role = relationship(
        "app.models.users.Roles",
        secondary="user_roles",
        backref="users",
    )
    order = relationship("app.models.orders.Orders", backref="users")
    subscriptions = relationship(
        "app.models.subscriptions.Subscriptions", backref="users"
    )
    reviews_and_ratings = relationship(
        "app.models.users.UserReviewsAndRatings",
        backref="users",
    )
    saved_items = relationship(
        "app.models.users.UserSavedItems",
        backref="users",
    )
    promotions = relationship(
        "app.models.UserPromotions", backref="users"
    )
    addresses = relationship(
        "app.models.users.UserAddresses", backref="users"
    )
    categories_for_user = relationship(
        "app.models.products.CategoriesForUser",
        backref="users",
    )
    data_privacy_consents = relationship(
        "app.models.users.DataPrivacyConsents",
        backref="users",
    )
    transactions = relationship(
        "app.models.orders.Transactions", backref="users"
    )
