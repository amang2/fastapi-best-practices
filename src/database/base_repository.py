from typing import Generic, TypeVar, Type, List, Optional

from sqlalchemy import and_, or_, select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import as_declarative

from src.exceptions import InvalidFieldError, DatabaseError

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    """Generic async repository for CRUD operations."""

    def __init__(self, model: Type[ModelT], session: AsyncSession):
        self.model = model
        self.session = session

    async def add(self, obj: ModelT) -> ModelT:
        try:
            self.session.add(obj)
            await self.session.flush()
            await self.session.refresh(obj)
            return obj
        except Exception as e:
            raise DatabaseError(f"Error adding {self.model.__name__}: {str(e)}")

    async def list_by(self, filters: dict = None) -> List[ModelT]:
        try:
            stmt = select(self.model).order_by(self.model.created_at.desc())
            if filters:
                conditions = [getattr(self.model, field) == value for field, value in filters.items()]
                stmt = stmt.where(and_(*conditions))
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise InvalidFieldError(f"Invalid field in filters: {str(e)}")
        
    
    
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


    async def delete_by_id(self, id) -> int:
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.rowcount