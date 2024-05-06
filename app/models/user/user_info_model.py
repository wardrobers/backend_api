from uuid import uuid4
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from ..basemixin import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    uuid = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, comment="Индетифекатор"
    )
    first_name = Column(String, nullable=False, comment="Имя")
    last_name = Column(String, nullable=True, comment="Фамилия")
    phone_number = Column(String, nullable=True, comment="Номер телефона")
    email = Column(String, nullable=False, comment="Почта")
    lender = Column(
        Boolean, nullable=False, default=False, comment="Лендер ли пользователь"
    )
    created_at = Column(DateTime, default=func.now(), comment="Создано")
    updated_at = Column(DateTime, onupdate=func.now(), comment="Отредактировано")
    deleted_at = Column(DateTime, nullable=True, comment="Удалено")

    # Foreign keys
    user_uuid = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid"),
        nullable=False,
        comment="Пользовтаель",
    )

    # Relationships
    user = relationship("User", backref="user_info")
