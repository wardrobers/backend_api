from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from uuid import uuid4

from ...common.base_model import Base


class TypesOfOperations(Base):
    __tablename__ = "types_of_operations"

    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    name = Column(String, nullable=True, default=None, comment="Наименование")
    created_at = Column(DateTime, nullable=True, default=func.now(), comment="Создано")
    updated_at = Column(
        DateTime, nullable=True, onupdate=func.now(), comment="Отредактировано"
    )
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Relationships
    articles = relationship("Article", backref="types_of_operations")
