from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.user_profile.repository import QuestionRepository, UserRepository
from src.user_profile.models import Question, QuestionOption, UserProfile
from src.user_profile.schemas import QuestionCreate, UserCreate
from src.utils.logger import service_logger


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def create_user(self, payload: UserCreate) -> UserProfile:
        """Create a new user."""
        service_logger.info(f"Creating user: {payload.email}")
        user = UserProfile(**payload.model_dump())
        created_user = await self.repo.add(user)
        service_logger.info(f"User created with id: {created_user.id}")
        return created_user
    
    async def list_users(self) -> List[UserProfile]:
        """List all users."""
        service_logger.info("Listing all users")
        users = await self.repo.list_by()
        service_logger.info(f"Total users found: {len(users)}")
        return users
    
class QuestionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = QuestionRepository(session)

    async def create_question(self, payload: QuestionCreate) -> QuestionCreate:
        """Create a new question."""
        service_logger.info(f"Creating question: {payload.text}")
        if payload.type == "single_choice" or payload.type == "multiple_choice":
            if not payload.options or len(payload.options) < 2:
                raise ValueError("At least two options are required for choice questions.")
        question = Question(
            text=payload.text,
            type=payload.type,
            que_order=payload.que_order,
            options=[QuestionOption(text=opt.text) for opt in (payload.options or [])],
            matrix_rows=payload.matrix_rows,
            matrix_cols=payload.matrix_cols
        )
        created_question = await self.repo.add(question)
        service_logger.info(f"Question created with id: {created_question.id}")
        return created_question
    
    async def list_questions(self) -> List[Question]:
        """List all questions."""
        service_logger.info("Listing all questions")
        questions = await self.repo.list_by()
        service_logger.info(f"Total questions found: {len(questions)}")
        return questions
    
    async def submit_answers(self, answers: List[dict]) -> List[Question]:
        """Submit user answers."""
        service_logger.info("Submitting user answers")
        # Implementation for submitting answers goes here
        service_logger.info("User answers submitted successfully")
        return []  # Return appropriate response