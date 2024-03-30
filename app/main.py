from fastapi import FastAPI, HTTPException, Request
from .database.session import db_engine, get_db, SessionLocal
from .models.basemixin import Base  # Adjust path as necessary


def create_tables():
    Base.metadata.create_all(bind=db_engine)


app = FastAPI(title="Wardrobers API", version="2.0")


@app.on_event("startup")
async def startup_event():
    create_tables()


# Middleware for DB session management
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = None
    request.state.db = SessionLocal()
    try:
        # Attach a new session to the request state
        response = await call_next(request)
    except Exception as e:
        # Handle exceptions and potentially roll back transactions here
        request.state.db.rollback()
        raise e
    finally:
        # Always close the session after the request is done
        request.state.db.close()
    return response


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    if "/docs" in request.url.path or "/openapi.json" in request.url.path:
        # Adjust the CSP specifically for the Swagger UI pages
        response.headers["Content-Security-Policy"] = (
            "default-src 'self';"
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"  # Allow Swagger UI scripts
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"  # Allow Swagger UI styles
            "img-src 'self' https://fastapi.tiangolo.com;"  # Allow images from Swagger UI
            "font-src 'self' https://cdn.jsdelivr.net;"  # Allow fonts from jsDelivr CDN
        )
    else:
        # Default CSP and other headers for all other routes
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = "default-src 'self';"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = "geolocation=(self), microphone=()"
    return response


@app.get("/", tags=["Root"])
async def root():
    return {"Welcome to the Wardrobers API!"}


@app.get("/healthz", tags=["Test"])
async def liveness_check():
    try:
        # 1. Database Connectivity
        with get_db() as db:
            # Test a simple query to verify the connection
            db.execute("SELECT 1")

        # 2. (Optional) External Dependency Checks
        # If Wardrobers relies on other services (e.g., image storage, third-party APIs)
        # Add checks to make API requests to those external dependencies here

        return {"status": "ok", "dependencies": {"database": "ok"}}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service Unavailable")


# Including routers
from app.routers import (
    auth_router,
    user_router,
    product_router,
    order_router,
)  # Adjust path as necessary

app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(product_router.router, prefix="/products", tags=["Products"])
app.include_router(order_router.router, prefix="/orders", tags=["Orders"])
