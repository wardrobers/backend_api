from fastapi import FastAPI
from app.routes import user_router, product_router, order_router, subscription_router, category_router, auth_router, common_router

app = FastAPI()

# Include the routers for different domains
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(product_router.router, prefix="/products", tags=["products"])
app.include_router(order_router.router, prefix="/orders", tags=["orders"])
app.include_router(subscription_router.router, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(category_router.router, prefix="/categories", tags=["categories"])
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
# Include more routers as your application grows

# Include common routes that don't belong to a specific domain
app.include_router(common_router.router, tags=["common"])
