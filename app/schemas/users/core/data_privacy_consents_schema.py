from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class DataPrivacyConsentBase(BaseModel):
    data_usage_consent: bool = False
    marketing_communications_consent: bool = False
    other_consent: Optional[bool] = None
    consent_date: datetime


class DataPrivacyConsentCreate(DataPrivacyConsentBase):
    pass


class DataPrivacyConsentRead(DataPrivacyConsentBase):
    id: UUID4
    user_id: UUID4
