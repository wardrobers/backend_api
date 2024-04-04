from fastapi import APIRouter
from .routers.user import user_router,user_test_router
from .routers.product import product_router
from .routers.order import order_router

api_router = APIRouter()


# Bundle router inclusions for clarity and centralized error handling
def include_api_routers():
    api_router.include_router(user_router.router, prefix="/users", tags=["Users"])
    api_router.include_router(user_test_router.router, prefix="/test/users", tags=["Users_test"])
    api_router.include_router(
        product_router.router, prefix="/products", tags=["Products"]
    )
    api_router.include_router(order_router.router, prefix="/orders", tags=["Orders"])
