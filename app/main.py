from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.routers.users import auth_router, users_router

app = FastAPI(title="Wardrobers API", version="2.0")


# @app.middleware("http")
# def security_headers_middleware(request: Request, call_next):
#     response = call_next(request)
#     if "/docs" in request.url.path or "/openapi.json" in request.url.path:
#         # Adjust the CSP specifically for the Swagger UI pages
#         response.headers["Content-Security-Policy"] = (
#             "default-src 'self';"
#             "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"  # Allow Swagger UI scripts
#             "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"  # Allow Swagger UI styles
#             "img-src 'self' https://fastapi.tiangolo.com;"  # Allow images from Swagger UI
#             "font-src 'self' https://cdn.jsdelivr.net;"  # Allow fonts from jsDelivr CDN
#         )
#     else:
#         # Default CSP and other headers for all other routes
#         response.headers["X-Frame-Options"] = "SAMEORIGIN"
#         response.headers["X-Content-Type-Options"] = "nosniff"
#         response.headers["Strict-Transport-Security"] = (
#             "max-age=31536000; includeSubDomains"
#         )
#         response.headers["Content-Security-Policy"] = "default-src 'self';"
#         response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
#         response.headers["X-XSS-Protection"] = "1; mode=block"
#         response.headers["Permissions-Policy"] = "geolocation=(self), microphone=()"
#     return response


@app.get("/", tags=["Root"])
def root():
    return {"Welcome to the Wardrobers API!"}


@app.get("/healthz", tags=["Test"])
def liveness_check(db_session: Session = Depends(get_db)):
    # try:
    # Database connectivity check
    result = db_session.execute(
        select(1)
    )  # Executing an query to check database connectivity
    result.fetchone()  # Optionally fetch the result to ensure complete execution

    # Optional: Check other external dependencies here
    # e.g., API calls to third-party services, connectivity checks to external data sources

    return {"status": "ok", "dependencies": {"database": "ok"}}


# except SQLAlchemyError as e:
#     # Specific database related errors can be caught and handled separately
#     raise HTTPException(status_code=503, detail=f"Database Unavailable: {str(e)}")
# except Exception as e:
#     # Catch-all for any other issues that occur during the health check
#     raise HTTPException(status_code=503, detail=f"Service Unavailable: {str(e)}")


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
