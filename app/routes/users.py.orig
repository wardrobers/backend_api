import datetime
import os
from hashlib import sha256
from operator import and_
from typing import Text

from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Query
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, relationship, sessionmaker
from sqlalchemy.sql.expression import delete

from app.dependencies import JWT_SECRET, get_current_user, get_db
from app.models.models import (
    PaginationQuery,
    SortingQuery,
    Token,
    User,
    UserActivity,
    UserActivityDelete,
    UserActivityList,
    UserDelete,
    UserInformation,
    UserList,
    UserLogin,
    UsersPhotos,
    UsersPhotosDelete,
    UsersPhotosList,
    UserSubscriptionType,
)
from app.models.sql import (
    Subscription,
    SubscriptionPeriod,
    SubscriptionType,
    User,
    UserActivity,
    UserInfo,
    UsersPhotos,
)

router = APIRouter()
DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.post("/register", response_model=Token)
def user_create(user_data: User, db: SessionLocal = Depends(get_db)):
    db_user = db.query(User).filter(User.login == user_data.login).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = sha256(user_data.password.encode()).hexdigest()
    new_user = User(
        login=user_data.login,
        password=hashed_password,
        is_notificated=user_data.is_notificated,
        last_login_at=datetime.now(),
        marketing_consent=user_data.marketing_consent,
        super_admin=user_data.super_admin,  # Если null = False
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(new_user)
    db.flush()
    new_user_info = UserInformation(
        user_uuid=new_user.uuid, **user_data.user_info.dict()
    )
    db.add(new_user_info)
    db.commit()

    token = JWT_SECRET.encode(
        {
            "sub": new_user.login,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        },
        JWT_SECRET,
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.login == user_data.login).first()
    if not user or sha256(user_data.password.encode()).hexdigest() != user.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = JWT_SECRET.encode(
        {
            "sub": user.login,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        },
        JWT_SECRET,
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/user/{uuid}", response_model=User)
def user_get(uuid: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.uuid == uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/users", response_model=UserList)
def user_list(
    deleted_at: bool = None,
    is_notificated: bool = None,
    last_login_at_start: datetime = None,
    last_login_at_end: datetime = None,
    super_admin: bool = None,
    created_at_start: datetime = None,
    created_at_end: datetime = None,
    name: str = None,
    surname: str = None,
    second_name: str = None,
    email: str = None,
    pagination: PaginationQuery = Depends(),
    sort: SortingQuery = Depends(),
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .order_by(Text(f"{sort.sort_by} {sort.order}"))
        .offset(pagination.skip)
        .limit(pagination.limit)
        .all()
    )
    # Filter deleted_at
    if deleted_at is not None:
        if deleted_at:
            query = Query.filter(User.deleted_at.isnot(None))
        else:
            query = Query.filter(User.deleted_at.is_(None))

    # Filter is_notificated
    if is_notificated is not None:
        query = query.filter(User.is_notificated == is_notificated)

    # Filter last_login_at
    if last_login_at_start is not None and last_login_at_end is not None:
        query = query.filter(
            and_(
                User.last_login_at >= last_login_at_start,
                User.last_login_at <= last_login_at_end,
            )
        )
    elif last_login_at_start is not None:
        query = query.filter(User.last_login_at >= last_login_at_start)
    elif last_login_at_end is not None:
        query = query.filter(User.last_login_at <= last_login_at_end)

    # Filter super_admin
    if super_admin is not None:
        query = query.filter(User.super_admin == super_admin)

    # Filter created_at
    if created_at_start is not None and created_at_end is not None:
        query = query.filter(
            and_(User.created_at >= created_at_start, User.created_at <= created_at_end)
        )
    elif created_at_start is not None:
        query = query.filter(User.created_at >= created_at_start)
    elif created_at_end is not None:
        query = query.filter(User.created_at <= created_at_end)

    # Filter user_info fields
    if name is not None:
        query = query.filter(User.user_info.name.ilike(f"%{name}%"))
    if surname is not None:
        query = query.filter(User.user_info.surname.ilike(f"%{surname}%"))
    if second_name is not None:
        query = query.filter(User.user_info.second_name.ilike(f"%{second_name}%"))
    if email is not None:
        query = query.filter(User.user_info.email.ilike(f"%{email}%"))

    return {"users": users}


@router.put("/user/{uuid}", response_model=User)
def user_update(uuid: str, user_data: User, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.uuid == uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.login = user_data.login
    user.super_admin = user_data.super_admin
    user.is_notificated = user_data.is_notificated
    user.last_login_at = user_data.last_login_at
    user.marketing_consent = user_data.marketing_consent
    user.updated_at = datetime.now()
    if user_data.user_info:
        user_info = db.query(UserInfo).filter(UserInfo.user_uuid == user.uuid).first()
        if not user_info:
            user_info = UserInfo(user_uuid=user.uuid)
        user_info.name = user_data.user_info.name
        user_info.surname = user_data.user_info.surname
        user_info.second_name = user_data.user_info.second_name
        user_info.email = user_data.user_info.email
        user_info.updated_at = datetime.now()
        db.add(user_info)

    db.commit()
    db.refresh(user)

    return user


@router.post("/user/{uuid}")
def user_delete(uuid: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.uuid == uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.deleted_at = datetime.now()
    db.commit()

    return {"message": "User marked as deleted"}
