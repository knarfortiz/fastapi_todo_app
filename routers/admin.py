from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from database import db_dependency
from models import Todos

from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return db.query(Todos).all()
