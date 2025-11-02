# src/database/base.py
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here so Alembic autogenerate can find them
from src.user import models as user_models


__all__ = ["Base"]
