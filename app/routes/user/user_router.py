# app/routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db, get_current_user
from .. import crud, models, schemas

router = APIRouter()

@router.get("/{uuid}", response_model=schemas.UserRead)
async def read_user(uuid: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, uuid=uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/update", response_model=schemas.UserRead)
async def update_user(user_update: schemas.UserUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_user(db=db, user=current_user, user_update=user_update)
