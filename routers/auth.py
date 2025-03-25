from fastapi import APIRouter
from passlib.context import CryptContext

from models import Users
from requests import CreateUserRequest

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/auth/")
async def get_user():
    return {"user": "authenticated"}


@router.post("/auth/")
async def create_user(user_request: CreateUserRequest):
    user = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        is_active=True,
    )

    return user
