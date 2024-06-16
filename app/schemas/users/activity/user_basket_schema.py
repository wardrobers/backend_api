from pydantic import UUID4, BaseModel


class UserBasketBase(BaseModel):
    count: int = 1


class UserBasketCreate(UserBasketBase):
    stock_keeping_unit_id: UUID4


class UserBasketRead(UserBasketBase):
    id: UUID4
    user_id: UUID4
    stock_keeping_unit_id: UUID4


# --- Resolving Forward References ---
UserBasketRead.model_rebuild()