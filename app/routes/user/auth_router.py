from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas.user.user_schema import UserRead, UserCreate
from ..repositories.user.user_repository import UserRepository
from ..security.auth_handler import AuthHandler

router = APIRouter()

# Initialize your AuthHandler
auth_handler = AuthHandler()

@router.post("/register", response_model=UserRead)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
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
    user = user_repo.create_user(user_data)
    return user

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    # Authenticate user
    user = user_repo.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # Create access token
    access_token = auth_handler.create_access_token(data={"sub": user.login})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-token", response_model=UserRead)
async def verify_token(token: str = Depends(auth_handler.oauth2_scheme), db: Session = Depends(get_db)):
    # Decode and verify the token
    user_info = auth_handler.verify_token(token, db)
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
    return user_info

