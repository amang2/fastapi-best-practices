from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError


from src.exceptions import AppException, DatabaseError
from src.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    global_exception_handler,
    database_exception_handler
)
from src.user_profile.controller import USER_SERVICE


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI App",
        description="Simple FastAPI application",
        version="1.0.0",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        openapi_url="/api/v1/openapi.json"
    )
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_exception_handler(DatabaseError, database_exception_handler)
    app.include_router(USER_SERVICE, prefix="/api/v1/user")
    return app