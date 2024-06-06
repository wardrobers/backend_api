from sqlalchemy import Boolean, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.repositories.common import Base, BaseMixin


class DataPrivacyConsents(Base, BaseMixin):
    __tablename__ = "data_privacy_consents"

    data_usage_consent = Column(Boolean, nullable=False, default=False)
    marketing_communications_consent = Column(Boolean, nullable=False, default=False)
    other_consent = Column(Boolean)
    consent_date = Column(DateTime)

    # Foreign keys
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
