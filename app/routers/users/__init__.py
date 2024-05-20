from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.authentication import AuthHandler
from app.routers.users.core import user_router, auth_router
from app.routers.users.activity import user_activity_router
from app.routers.users.roles import user_roles_router
from app.routers.users.subscriptions import user_subscriptions_router
from app.routers.users.profile import user_photos_router, user_addresses_router

# Initialize OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create the main routers
users_router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(oauth2_scheme)]
)
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Initialize the AuthHandler
auth_handler = AuthHandler()

# Include all auth and user-related sub-routers
auth_router.include_router(auth_router.router)
users_router.include_router(user_router.router)
users_router.include_router(user_activity_router.router)
users_router.include_router(user_roles_router.router)
users_router.include_router(user_subscriptions_router.router)
users_router.include_router(user_photos_router.router)
users_router.include_router(user_addresses_router.router)
