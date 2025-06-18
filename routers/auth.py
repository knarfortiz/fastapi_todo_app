from datetime import datetime, timedelta, timezone
from typing import Annotated
from urllib import response

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users
from requests import CreateUserRequest
from responses import Token

router = APIRouter()

SECRET_KEY = "030993fb623822b969f4b7d5e40ac517762a5df692064b54cf3c9ae62baeec13"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(db: db_dependency, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.get("/auth")
async def get_user():
    return {"user": "authenticated"}


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: CreateUserRequest):
    user = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(
        user.username, user.id, expires_delta=timedelta(minutes=20)
    )

    return Token(access_token=token, token_type="bearer")
