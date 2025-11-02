from typing import List, Optional

from .models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.base_repository import BaseRepository
from .models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)