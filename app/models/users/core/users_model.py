from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

# Import models that are directly related and need explicit import for relationships
from app.models.common.base_model import Base, BaseMixin
from app.models.common.bulk_actions_model import BulkActionsMixin
from app.models.common.cache_model import CachingMixin
from app.models.common.search_model import SearchMixin


class Users(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
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
        "app.models.users.activity.user_activity_model.UserActivity",
        uselist=False,
        backref="users",
    )
    basket = relationship(
        "app.models.users.profile.user_basket_model.UserBasket",
        uselist=False,
        backref="users",
    )
    photos = relationship(
        "app.models.users.profile.user_photos_model.UserPhotos", backref="users"
    )
    role = relationship(
        "app.models.users.roles.roles_model.Roles",
        secondary="user_roles",
        backref="users",
    )
    order = relationship("app.models.orders.core.order_model.Orders", backref="users")
    subscriptions = relationship(
        "app.models.subscriptions.subscriptions_model.Subscriptions", backref="users"
    )
    reviews_and_ratings = relationship(
        "app.models.users.activity.user_reviews_and_ratings_model.UserReviewsAndRatings",
        backref="users",
    )
    saved_items = relationship(
        "app.models.users.activity.user_saved_items_model.UserSavedItems",
        backref="users",
    )
    promotions = relationship(
        "app.models.promotions.user_promotions_model.UserPromotions", backref="users"
    )
    addresses = relationship(
        "app.models.users.profile.user_addresses_model.UserAddresses", backref="users"
    )
    categories_for_user = relationship(
        "app.models.products.product_details.category_model.CategoriesForUser",
        backref="users",
    )
    data_privacy_consents = relationship(
        "app.models.users.core.data_privacy_consents_model.DataPrivacyConsents",
        backref="users",
    )
    transactions = relationship(
        "app.models.orders.payments.transactions_model.Transactions", backref="users"
    )
