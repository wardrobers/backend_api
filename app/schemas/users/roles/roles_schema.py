from pydantic import UUID4, BaseModel


class RoleBase(BaseModel):
    code: str
    name: str


class RoleRead(RoleBase):
    id: UUID4


class RoleAssign(BaseModel):
    role_id: UUID4
