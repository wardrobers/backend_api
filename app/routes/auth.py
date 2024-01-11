import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, relationship
from ..models.pydantic import UserLogin, UserCreate, Token
from ..dependencies import get_db, get_current_user
from ..models.sqlalchemy import User
from hashlib import sha256

router = APIRouter()
DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = db.query(User).filter(User.login == user_data.login).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = sha256(user_data.password.encode()).hexdigest()
    new_user = User(
        login=user_data.login,
        password=hashed_password,
        is_notificated=user_data.is_notificated,
    )
    db.add(new_user)
    db.flush()  # Flush to retrieve the generated UUID for new_user

    new_user_info = UserInfo(user_uuid=new_user.uuid, **user_data.user_info.dict())
    db.add(new_user_info)
    db.commit()

    token = jwt.encode(
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

    token = jwt.encode(
        {
            "sub": user.login,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        },
        JWT_SECRET,
    )
    return {"access_token": token, "token_type": "bearer"}
