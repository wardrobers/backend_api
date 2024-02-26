from fastapi import APIRouter
from app.routers import user_router, product_router, order_router, subscription_router, static_router

api_router = APIRouter()

# Authentication and User Management
api_router.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router.router, prefix="/users", tags=["Users"])

# Product Catalog and Management
api_router.include_router(product_router.router, prefix="/products", tags=["Products"])
api_router.include_router(category_router.router, prefix="/categories", tags=["Categories"])
api_router.include_router(material_router.router, prefix="/materials", tags=["Materials"])
api_router.include_router(color_router.router, prefix="/colors", tags=["Colors"])
api_router.include_router(size_router.router, prefix="/sizes", tags=["Sizes"])

# Order Management
api_router.include_router(order_router.router, prefix="/orders", tags=["Orders"])

# Subscription Management
api_router.include_router(subscription_router.router, prefix="/subscriptions", tags=["Subscriptions"])

