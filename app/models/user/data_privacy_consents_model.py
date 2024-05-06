from sqlalchemy import Column, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, backref
from sqlalchemy.sql import func
from uuid import uuid4

from ..basemixin import Base


class DataPrivacyConsents(Base):
    __tablename__ = "data_privacy_consents"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    data_usage_consent = Column(Boolean, nullable=False, default=False)
    marketing_communications_consent = Column(Boolean, nullable=False, default=False)
    other_consent = Column(Boolean)
    consent_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Foreign keys
    user_uuid = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )

    # Relationship
    user = relationship("User", backref=backref("data_privacy_consents", uselist=True))
