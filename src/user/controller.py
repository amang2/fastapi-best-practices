from fastapi import APIRouter, Depends
from ..dependency import get_user_service
from .service import UserService
from .schemas import UserCreate, UserRead

USER_SERVICE = APIRouter()


@USER_SERVICE.get("/list", response_model=list[UserRead], tags=["user"])
async def list_users(service: UserService = Depends(get_user_service)):
    users = await service.list_users()
    return users


@USER_SERVICE.post("/create", response_model=UserRead, tags=["user"])
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    user = await service.create_user(payload.name)
    return user

