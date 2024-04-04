import datetime
from multiprocessing import get_context
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import UUID4
from ...database.session import get_db
from hashlib import sha256
from ...schemas.user.user_test_schema import UserrLoginResponse,UserrLoginRequest, UserrResponse, UserrCreateRequest, UserrCreateResponse, UserrGetResponse
from ...models.user.user_test_model import Userr, UserrInfo, UserrPhoto, UserrRole, Roler

router = APIRouter()


# User registration
@router.post("/register", response_model=UserrCreateResponse)
async def register_user(user_create: UserrCreateRequest, request: Request):
    db: Session = request.state.db
    user_instance = db.query(Userr).filter(Userr.login == user_create.login).first()
    if user_instance:
        raise HTTPException(status_code=400, detail="1-0-0-0: User already exists")
    
    hashed_password = get_context.hash(user_create.password)
    new_user = Userr(
        login=user_create.login,
        hashed_password=hashed_password,
        is_notificated=user_create.is_notificated,
        marketing_consent=user_create.marketing_consent
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserrResponse(uuid=new_user.uuid, login=new_user.login, created_at=new_user.created_at)


@router.post("/login", response_model=UserrLoginResponse)
async def login_for_access_token(user_login: UserrLoginRequest, request: Request):
    db: Session = request.state.db
    user = db.query(Userr).filter(Userr.login == user_login.login).first()
    if not user:
        raise HTTPException(status_code=400, detail="1-0-0-3: User with this login does not exist")
    if not get_context.verify(user_login.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="1-0-0-4: Incorrect password")
    user.last_login_at = datetime.utcnow()
    db.commit()

    return {"uuid": user.uuid, "last_login_at": user.last_login_at}

@router.post("/get", response_model=UserrGetResponse)
async def get_user_data(user_uuid: UUID4, request: Request):
    db: Session = request.state.db
    user = db.query(Userr).filter(Userr.uuid == user_uuid, Userr.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    user_data, user_info, user_photo, user_role = user
    response = {
        "uuid": user.uuid,
        "login": user.login,
        "is_notificated": user.is_notificated,
        "marketing_consent": user.marketing_consent,
        "created_at": user.created_at,
        "info": {
            "name": user.info.name,
            "last_name": user.info.last_name,
            "email": user.info.email
        } if user.info else {},
        "photos": [
            {"uuid": photo.uuid, "storage_url": photo.storage_url}
            for photo in user.photos  # Access photos directly from the user
        ] if user.photos else [],
        "roles": [
            {"uuid": role.role_uuid, "code": role.code, "name": role.name}
            for role in user.roles  # Access roles directly from the user
        ] if user.roles else [],
    }

    return response