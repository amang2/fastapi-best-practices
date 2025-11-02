from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from .repository import UserRepository
from .models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def list_users(self) -> List[User]:
        return await self.repo.get_all()

    async def create_user(self, name: str) -> User:
        user = User(name=name)
        return await self.repo.add(user)
