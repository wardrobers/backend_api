from enum import Enum
from typing import Optional

from pydantic import UUID4, BaseModel


class RoleAction(str, Enum):
    ADD = "add"
    REMOVE = "remove"


class RoleBase(BaseModel):
    code: str
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    code: Optional[str] = None
    name: Optional[str] = None


class RoleRead(RoleBase):
    id: UUID4


class RoleAssign(BaseModel):
    role_id: UUID4
