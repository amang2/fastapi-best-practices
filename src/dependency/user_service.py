from typing import AsyncGenerator

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from ..database.database import get_async_session
from ..user.service import UserService


async def get_user_service(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[UserService, None]:
    """Dependency that yields a UserService with an injected DB session."""
    service = UserService(session)
    try:
        yield service
    finally:
        await session.close()





