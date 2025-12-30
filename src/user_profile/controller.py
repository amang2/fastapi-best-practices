from typing import List
from fastapi import APIRouter, Depends, status
from src.dependency.question_service import get_question_service
from src.dependency.user_service import get_user_service
from src.user_profile.service import QuestionService, UserService
from src.user_profile.schemas import QuestionCreate, QuestionRead, UserCreate, UserRead
from src.utils.logger import controller_logger


USER_SERVICE = APIRouter()


@USER_SERVICE.post("/create", response_model=UserRead, tags=["User"], status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """Create a new user."""
    controller_logger.info(f"Creating user: {payload.email}")
    user = await service.create_user(payload)
    controller_logger.info(f"User created with id: {user.id}")
    return user


@USER_SERVICE.post("/list", response_model=List[UserRead], tags=["User"], status_code=status.HTTP_200_OK)
async def list_users(
    service: UserService = Depends(get_user_service)
):
    """List all users."""
    controller_logger.info("Listing all users")
    users = await service.list_users()
    controller_logger.info(f"Total users found: {len(users)}")
    return users

@USER_SERVICE.post("/question/create", response_model=QuestionRead, tags=["Questions"], status_code=status.HTTP_201_CREATED)
async def list_users(
    payload: QuestionCreate,
    service: QuestionService = Depends(get_question_service)
):
    """Create Question."""
    controller_logger.info("Listing all users")
    que = await service.create_question(payload)
    controller_logger.info(f"Total users found: {que}")
    return que

@USER_SERVICE.post("/question/list", response_model=List[QuestionRead], tags=["Questions"], status_code=status.HTTP_200_OK)
async def list_users(
    service: QuestionService = Depends(get_question_service)
):
    """List Question."""
    controller_logger.info("Listing all users")
    que = await service.list_questions()
    controller_logger.info(f"Total users found: {que}")
    return que

@USER_SERVICE.post("/question/submit", response_model=List[QuestionRead], tags=["Questions"], status_code=status.HTTP_200_OK)
async def submit_answers(
    service: QuestionService = Depends(get_question_service)
):
    """Submit Answers."""
    controller_logger.info("Listing all users")
    que = await service.list_questions()
    controller_logger.info(f"Total users found: {que}")
    return que