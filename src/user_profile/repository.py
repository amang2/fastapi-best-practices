from sqlalchemy.ext.asyncio import AsyncSession
from src.database.base_repository import BaseRepository
from src.user_profile.models import Question, UserProfile


class UserRepository(BaseRepository[UserProfile]):
    def __init__(self, session: AsyncSession):
        super().__init__(UserProfile, session)

class QuestionRepository(BaseRepository[Question]):
    def __init__(self, session: AsyncSession):
        super().__init__(Question, session)