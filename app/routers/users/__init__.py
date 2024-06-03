from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.routers.users.core import auth_router, user_router
from app.routers.users.profile import user_addresses_router, user_photos_router
from app.routers.users.subscriptions import user_subscriptions_router

# Initialize OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create the main routers
users_router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(oauth2_scheme)]
)
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Include all auth and user-related sub-routers
auth_router.include_router(auth_router.router)
users_router.include_router(user_router.router)
users_router.include_router(user_subscriptions_router.router)
users_router.include_router(user_photos_router.router)
users_router.include_router(user_addresses_router.router)
