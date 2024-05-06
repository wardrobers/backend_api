from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class ProductTypes(Base):
    __tablename__ = "product_types"

    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    created_at = Column(
        DateTime, nullable=False, server_default=func.now(), comment="Создано"
    )
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Foreign Keys
    product_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.uuid"), nullable=False, comment="Товар"
    )
    type_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("types.uuid"), nullable=False, comment="Тип вещи"
    )
