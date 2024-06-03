from datetime import datetime

from pydantic import UUID4, BaseModel


class UserSavedItemBase(BaseModel):
    article: str


class UserSavedItemCreate(UserSavedItemBase):
    article_id: UUID4


class UserSavedItemRead(UserSavedItemBase):
    id: UUID4
    user_id: UUID4
    article_id: UUID4
    saved_at: datetime
