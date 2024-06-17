from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, and_
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.types import Enum as SQLAEnum

from app.models.base_model import Base
from app.models.orders.payments.lender_payments_model import LenderPayments
from app.models.products.inventorization.specifications_model import Specifications
from app.models.products.maintenance.cleaning_logs_model import CleaningLogs
from app.models.products.maintenance.repair_logs_model import RepairLogs
from app.models.users.activity.user_saved_items_model import UserSavedItems


class OwnerType(str, Enum):
    Platform = "Platform"
    Lender = "Lender"
    Brands = "Brands"
    Partner = "Partner"


class Condition(str, Enum):
    New = "New"
    Excellent = "Excellent"
    Good = "Good"
    Fair = "Fair"
    Poor = "Poor"


class Articles(Base):
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
        UUID(as_uuid=True),
        ForeignKey("article_status.id"),
        nullable=False,
    )
    types_of_operation_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("types_of_operations.id"),
        nullable=False,
    )

    # Relationships
    specification = relationship(
        "Specifications",
        backref="articles",
    )
    cleaning_logs = relationship(
        "CleaningLogs",
        backref="articles",
        cascade="all, delete-orphan",
    )
    repair_logs = relationship(
        "RepairLogs",
        backref="articles",
        cascade="all, delete-orphan",
    )
    lender_payments = relationship(
        "LenderPayments",
        backref="articles",
    )
    order_items = relationship("OrderItems", backref="articles")
