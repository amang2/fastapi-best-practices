
from typing import Optional, Any, Dict


class AppException(Exception):
    """Base exception for all application errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize application exception.
        
        Args:
            message: Human-readable error message
            status_code: HTTP status code
            error_code: Machine-readable error code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppException):
    """Input validation failed."""
    
    def __init__(
        self,
        message: str,
        error_code: str = "VALIDATION_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=400,
            error_code=error_code,
            details=details
        )


class DuplicateResourceError(AppException):
    """Resource already exists."""
    
    def __init__(
        self,
        resource_type: str,
        resource_name: str,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"{resource_type} '{resource_name}' already exists"
        super().__init__(
            message=message,
            status_code=400,
            error_code="DUPLICATE_RESOURCE",
            details=details or {"resource_type": resource_type, "resource_name": resource_name}
        )


class ResourceNotFoundError(AppException):
    """Resource not found."""
    
    def __init__(
        self,
        resource_type: str,
        resource_id: Any,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(
            message=message,
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
            details=details or {"resource_type": resource_type, "resource_id": str(resource_id)}
        )


class InvalidFieldError(AppException):
    """Invalid field name provided."""
    
    def __init__(
        self,
        field_name: str,
        available_fields: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Invalid field '{field_name}'"
        if available_fields:
            message += f". Available fields: {', '.join(available_fields)}"
        
        super().__init__(
            message=message,
            status_code=400,
            error_code="INVALID_FIELD",
            details=details or {
                "field_name": field_name,
                "available_fields": available_fields
            }
        )


class InvalidOperatorError(AppException):
    """Invalid operator provided."""
    
    def __init__(
        self,
        operator: str,
        supported_operators: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Invalid operator '{operator}'"
        if supported_operators:
            message += f". Supported operators: {', '.join(supported_operators)}"
        
        super().__init__(
            message=message,
            status_code=400,
            error_code="INVALID_OPERATOR",
            details=details or {
                "operator": operator,
                "supported_operators": supported_operators
            }
        )


class InvalidSortOrderError(AppException):
    """Invalid sort order provided."""
    
    def __init__(
        self,
        sort_order: str,
        details: Optional[Dict[str, Any]] = None
    ):
        message = f"Invalid sort order '{sort_order}'. Must be 'asc' or 'desc'"
        super().__init__(
            message=message,
            status_code=400,
            error_code="INVALID_SORT_ORDER",
            details=details or {"sort_order": sort_order}
        )


class DatabaseError(AppException):
    """Database operation failed."""
    
    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code="DATABASE_ERROR",
            details=details or {"operation": operation} if operation else {}
        )


class UnauthorizedError(AppException):
    """Authentication required."""
    
    def __init__(
        self,
        message: str = "Authentication required",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=401,
            error_code="UNAUTHORIZED",
            details=details
        )


class ForbiddenError(AppException):
    """Access denied."""
    
    def __init__(
        self,
        message: str = "Access denied",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=403,
            error_code="FORBIDDEN",
            details=details
        )


class ConfigurationError(AppException):
    """Configuration is invalid."""
    
    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=500,
            error_code="CONFIGURATION_ERROR",
            details=details or {"config_key": config_key} if config_key else {}
        )


# Mapping of error codes to HTTP status codes for reference
ERROR_CODE_TO_STATUS = {
    "VALIDATION_ERROR": 400,
    "DUPLICATE_RESOURCE": 400,
    "INVALID_FIELD": 400,
    "INVALID_OPERATOR": 400,
    "INVALID_SORT_ORDER": 400,
    "RESOURCE_NOT_FOUND": 404,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "DATABASE_ERROR": 500,
    "CONFIGURATION_ERROR": 500,
    "INTERNAL_ERROR": 500,
}
