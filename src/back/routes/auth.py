from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import (
    APIRouter,
    Body,
    status,
    Depends
)

from schemas import UserCreate, CreatedResponse, UserExistsResponse
from services import HashingService as HS
from orm import UserORM
from exceptions import UserAlreadyExists
from dependencies import get_async_session


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@router.post("/signup", response_model=CreatedResponse, status_code=status.HTTP_201_CREATED)
async def sign_up(
        user_creds: Annotated[UserCreate, Body()],
        db_session: AsyncSession = Depends(get_async_session)
):
    user = await UserORM.select_user_by_username(user_creds.username, db_session)
    if user:
        raise UserAlreadyExists(user_creds.username)
    else:
        user_creds.hashed_password = HS.encrypt(user_creds.hashed_password)
        await UserORM.create_user(user_creds, db_session)
        return CreatedResponse()

