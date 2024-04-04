from pydantic import BaseModel, UUID4, Field
from typing import Optional, List
from datetime import datetime



class UserrCreate(BaseModel):
    login: str
    password: str
    is_notificated: Optional[bool] = False
    marketing_consent: Optional[bool] = False

class UserrResponse(BaseModel):
    uuid: str
    login: str
    created_at: datetime

class UserrCreateRequest(BaseModel):
    login: str
    password: str
    is_notificated: Optional[bool] = False
    marketing_consent: Optional[bool] = False

class UserrCreateResponse(BaseModel):
    uuid: UUID4
    login: str
    created_at: datetime

# Models for User Login
class UserrLoginRequest(BaseModel):
    login: str
    password: str

class UserrLoginResponse(BaseModel):
    uuid: UUID4
    last_login_at: datetime

# Models for User Information Retrieval
class UserrInfoResponse(BaseModel):
    name: str
    last_name: Optional[str]
    email: str

class UserrPhotoResponse(BaseModel):
    uuid: UUID4
    storage_url: str

class UserrRoleResponse(BaseModel):
    uuid: UUID4
    code: str
    name: str

class UserrGetResponse(BaseModel):
    uuid: UUID4
    login: str
    is_notificated: bool
    marketing_consent: bool
    created_at: datetime
    info: Optional[UserrInfoResponse]
    photos: List[UserrPhotoResponse]
    roles: List[UserrRoleResponse]