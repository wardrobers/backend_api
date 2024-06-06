from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.models import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=False)
    lender = Column(Boolean, nullable=False, default=False)

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
