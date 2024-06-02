from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.common import (
    Base,
    BaseMixin,
    BulkActionsMixin,
    CachingMixin,
    SearchMixin,
)


class OwnerType(Enum):
    Platform = "Platform"
    Lender = "Lender"
    Brand = "Brand"
    Partner = "Partner"


class Condition(Enum):
    New = "New"
    Excellent = "Excellent"
    Good = "Good"
    Fair = "Fair"
    Poor = "Poor"


class Articles(Base, BaseMixin, SearchMixin, CachingMixin, BulkActionsMixin):
    __tablename__ = "articles"

    article = Column(String, nullable=False)
    owner_type = Column(SQLAEnum(OwnerType), nullable=False)
    factory_number = Column(String, nullable=True)
    times_used = Column(Integer, nullable=False, default=0)
    hours_used = Column(Integer, nullable=False, default=0)
    min_rental_days = Column(Integer, nullable=False, default=2)
    buffer_days = Column(Integer, nullable=False, default=1)
    pre_rental_buffer = Column(Integer, nullable=True, default=0)
    for_cleaning = Column(Boolean, nullable=True, default=False)
    for_repair = Column(Boolean, nullable=True, default=False)
    condition = Column(SQLAEnum(Condition), nullable=False)

    # Foreign keys
    sku_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("stock_keeping_units.id"),
        nullable=False,
    )
    status_code = mapped_column(
        String,
        ForeignKey("article_status.status_code"),
        nullable=False,
    )
    types_of_operation_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("types_of_operations.id"),
        nullable=False,
    )

    # Relationships
    specification = relationship(
        "app.model.products.maintenance.specifications_model.Specifications",
        backref="articles",
    )
    cleaning_logs = relationship(
        "app.model.products.maintenance.cleaning_log_model.CleaningLogs",
        backref="articles",
    )
    repair_logs = relationship(
        "app.model.products.maintenance.repair_log_model.RepairLogs", backref="articles"
    )
    lender_payments = relationship(
        "app.model.orders.payments.lender_payments_model.LenderPayments",
        backref="articles",
    )
    user_saved_items = relationship(
        "app.model.users.activity.user_saved_items_model.UserSavedItems",
        backref="articles",
    )
    order_items = relationship(
        "app.model.orders.core.order_items_model.OrderItems", backref="articles"
    )
