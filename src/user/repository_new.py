from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from ..database.base_repository import BaseRepository
from .models import User


class UserRepository(BaseRepository[User]):
    """Simple UserRepository that inherits BaseRepository CRUD methods.

    Override any BaseRepository methods here when custom behavior is required.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    # Example override (optional):
    # async def get_all(self) -> List[User]:
    #     # custom logic here
    #     return await super().get_all()
