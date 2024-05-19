from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_async_session
from app.models.common import Base
from app.routers.users import users_router, auth_router


app = FastAPI(title="Wardrobers API", version="2.0")


@app.on_event("startup")
async def startup_event():
    async with get_async_session() as session:
        await session.run_sync(Base.metadata.create_all)


# Middleware for DB session management
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = None
    request.state.db = await get_async_session()
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
async def liveness_check(db_session: AsyncSession = Depends(get_async_session)):
    try:
        # Database connectivity check
        result = await db_session.execute(
            select(1)
        )  # Executing an async query to check database connectivity
        result.fetchone()  # Optionally fetch the result to ensure complete execution

        # Optional: Check other external dependencies here
        # e.g., API calls to third-party services, connectivity checks to external data sources

        return {"status": "ok", "dependencies": {"database": "ok"}}
    except SQLAlchemyError as e:
        # Specific database related errors can be caught and handled separately
        raise HTTPException(status_code=503, detail=f"Database Unavailable: {str(e)}")
    except Exception as e:
        # Catch-all for any other issues that occur during the health check
        raise HTTPException(status_code=503, detail=f"Service Unavailable: {str(e)}")


app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(users_router.router, prefix="/users", tags=["Users"])
