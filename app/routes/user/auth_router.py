# app/routers/auth_router.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..dependencies import get_db
from .. import crud, models, schemas
from ..security import create_access_token, verify_password, get_current_user

router = APIRouter()

@router.post("/register", response_model=schemas.UserRead)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: schemas.UserLoginForm, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-token", response_model=schemas.UserRead)
async def verify_token(current_user: models.User = Depends(get_current_user)):
    return current_user