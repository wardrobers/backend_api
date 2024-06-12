from fastapi import APIRouter, Depends

from app.repositories.users import AuthRepository

from .core.auth_router import router as auth_router
from .core.user_router import router as user_router
from .profile.user_addresses_router import router as user_addresses_router
from .profile.user_photos_router import router as user_photos_router
from .roles.user_roles import router as user_roles_router

# Include all user-related sub-routers
users_router = APIRouter(prefix="/users", tags=["Users"])
users_router.include_router(
    user_router, dependencies=[Depends(AuthRepository.get_current_user)]
)
users_router.include_router(
    user_roles_router, dependencies=[Depends(AuthRepository.get_current_user)]
)
users_router.include_router(
    user_photos_router, dependencies=[Depends(AuthRepository.get_current_user)]
)
users_router.include_router(
    user_addresses_router, dependencies=[Depends(AuthRepository.get_current_user)]
)

__all__ = [
    "auth_router",
    "user_router",
    "user_addresses_router",
    "user_photos_router",
    "user_roles_router",
]
