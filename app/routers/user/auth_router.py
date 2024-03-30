from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from ...database.session import get_db
from ...schemas.user.user_schema import UserRead, UserCreate
from ...schemas.user.user_info_schema import UserInfoCreate
from ...repositories.user.user_repository import UserRepository
from ...authentication.security import AuthHandler

router = APIRouter()

# Initialize your AuthHandler
auth_handler = AuthHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=UserRead)
def register_user(
    user_create: UserCreate,
    request: Request,
    user_info_create: Optional[UserInfoCreate] = None,
):
    db: Session = request.state.db
    user_repo = UserRepository(db)
    # Check if user already exists by login
    if user_repo.get_user_by_login(user_create.login):
        raise HTTPException(status_code=400, detail="Login already in use")
    # Hash password
    hashed_password = auth_handler.get_password_hash(user_create.password)
    # Adjust user creation data to include hashed password
    user_data = user_create.dict()
    user_data["password"] = hashed_password
    # Create user
    user = user_repo.create_user(user_data, user_info_create)
    return user


@router.post("/login")
async def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
):
    db: Session = request.state.db
    user_repo = UserRepository(db)
    # Authenticate user
    user = user_repo.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Create access token
    access_token = auth_handler.create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-token", response_model=UserRead)
async def verify_token(request: Request, token: str = Depends(oauth2_scheme)):
    db: Session = request.state.db
    # Decode and verify the token
    user_info = auth_handler.verify_token(token, db)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
    return user_info
