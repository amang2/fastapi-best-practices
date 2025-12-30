from typing import AsyncGenerator

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.postgres_conn import get_async_session
from src.user_profile.service import QuestionService


async def get_question_service(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[QuestionService, None]:
    return QuestionService(session)

