import traceback
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .exceptions import AppException, DatabaseError
from .utils.logger import logger


class ErrorResponse:
    @staticmethod
    def format(
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: dict = None,
        request_id: str = None
    ) -> dict:
        return {
            "success": False,
            "message": message,
            "error_code": error_code,
            "status_code": status_code,
            "details": details or {},
            "request_id": request_id
        }


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    error_response = ErrorResponse.format(
        message=exc.message,
        error_code=exc.error_code,
        status_code=exc.status_code,
        details=exc.details,
        request_id=request.headers.get("X-Request-ID")
    )
    
    log_message = f"{exc.error_code}: {exc.message}"
    
    if exc.status_code >= 500:
        logger.error(
            log_message,
            extra={
                "error_code": exc.error_code,
                "status_code": exc.status_code,
                "details": exc.details,
                "path": request.url.path,
                "method": request.method
            }
        )
    else:
        logger.warning(
            log_message,
            extra={
                "error_code": exc.error_code,
                "status_code": exc.status_code,
                "details": exc.details,
                "path": request.url.path,
                "method": request.method
            }
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    errors = {}
    for error in exc.errors():
        field = error["loc"][-1] if error["loc"] else "body"
        errors[field] = error["msg"]
    
    error_response = ErrorResponse.format(
        message="Request validation failed",
        error_code="VALIDATION_ERROR",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details={"validation_errors": errors},
        request_id=request.headers.get("X-Request-ID")
    )
    
    logger.warning(
        "Validation error",
        extra={
            "error_code": "VALIDATION_ERROR",
            "validation_errors": errors,
            "path": request.url.path,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response
    )


async def global_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    error_response = ErrorResponse.format(
        message="An unexpected error occurred",
        error_code="INTERNAL_ERROR",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        details={},
        request_id=request.headers.get("X-Request-ID")
    )
    
    logger.error(
        f"Unexpected error: {str(exc)}",
        extra={
            "error_code": "INTERNAL_ERROR",
            "exception_type": type(exc).__name__,
            "traceback": traceback.format_exc(),
            "path": request.url.path,
            "method": request.method
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )



async def database_exception_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    # Format the response consistently with ErrorResponse
    error_response = ErrorResponse.format(
        message=exc.message,
        error_code=exc.error_code,
        status_code=exc.status_code,
        details=exc.details,
        request_id=request.headers.get("X-Request-ID")
    )

    # Log the error for debugging
    logger.error(
        f"Database error: {exc.message}",
        extra={
            "error_code": exc.error_code,
            "exception_type": type(exc).__name__,
            "details": exc.details,
            "traceback": traceback.format_exc(),
            "path": request.url.path,
            "method": request.method
        }
    )

    # Return JSON response
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )