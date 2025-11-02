from typing import Generic, TypeVar, Type, List, Optional

from sqlalchemy import and_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import as_declarative

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    """Generic async repository providing basic CRUD operations.

    Usage:
        class UserRepository(BaseRepository[User]):
            def __init__(self, session: AsyncSession):
                super().__init__(User, session)
    """

    def __init__(self, model: Type[ModelT], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self) -> List[ModelT]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, id) -> Optional[ModelT]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().first()
    
    async def get_by(self, **filters) -> Optional[ModelT]:
        stmt = select(self.model)
        if filters:
            conditions = [getattr(self.model, field) == value for field, value in filters.items()]
            stmt = stmt.where(and_(*conditions))
        result = await self.session.execute(stmt)
        return result.scalars().first()
    

    async def add(self, obj: ModelT) -> ModelT:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def delete_by_id(self, id) -> int:
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.rowcount
