from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_dict = {}
    for error in exc.errors():
        loc = error.get("loc", [])
        field = loc[-1] if len(loc) > 1 else "body"
        msg = error.get("msg")
        error_dict.setdefault(field, []).append(msg)
    
    response = APIResponse.error_response(
        message="Validation failed",
        errors=error_dict,
        meta=MetaModel(path=str(request.url))
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.dict()  # Use dict() to serialize datetime
    )

# 500 Global Exception Handler
async def global_exception_handler(request: Request, exc: Exception):
    response = APIResponse.error_response(
        message="Internal server error",
        errors=[str(exc)],
        meta=MetaModel(path=str(request.url))
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.dict()  # Use dict() to serialize datetime
    )


# --- Meta & Common Response Schema ---
class MetaModel(BaseModel):
    timestamp: datetime = datetime.utcnow()
    path: Optional[str] = None

    def dict(self, **kwargs):
        # Convert datetime to ISO string
        d = super().model_dump(**kwargs)
        d["timestamp"] = d["timestamp"].isoformat()
        return d


class ApiStandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[Union[Dict[str, List[str]], List[str]]] = None
    meta: Optional[MetaModel] = None

    def dict(self, **kwargs):
        # Serialize MetaModel properly
        d = super().model_dump(**kwargs)
        if self.meta:
            d["meta"] = self.meta.dict()
        return d

    @classmethod
    def success_response(
        cls, message: str, data: Any = None, meta: Optional[MetaModel] = None
    ):
        return cls(
            success=True,
            message=message,
            data=data,
            meta=meta or MetaModel()
        )

    @classmethod
    def error_response(
        cls,
        message: str,
        errors: Optional[Union[Dict[str, List[str]], List[str]]] = None,
        meta: Optional[MetaModel] = None
    ):
        return cls(
            success=False,
            message=message,
            errors=errors,
            meta=meta or MetaModel()
        )
