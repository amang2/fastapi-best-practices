"""Dependency package for app-level dependencies."""

__all__ = ["get_async_session", "init_db", "get_user_service"]

from ..database.database import get_async_session, init_db
from .user_service import get_user_service
