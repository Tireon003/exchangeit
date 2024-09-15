from fastapi import (
    APIRouter,
    Depends,
    Path,
    status,
    Body,

)

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_async_session
from schemas import UserFromDB, AdCreate, CreatedResponse
from orm import UserORM, AdsORM
from exceptions import UserNotFoundException

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.get("/{user_id}", response_model=UserFromDB, status_code=status.HTTP_200_OK)
async def get_user(
        user_id: Annotated[int, Path()],
        db_session: AsyncSession = Depends(get_async_session)
):
    user = await UserORM.select_user_by_id(
        user_id=user_id,
        session=db_session,
    )
    if user:
        return user
    else:
        raise UserNotFoundException(user_id)


@router.post("/{user_id}/ads/new", response_model=CreatedResponse)
async def create_ad(
        ad_data: Annotated[AdCreate, Body()],
        user_id: Annotated[int, Path()],
        db_session: AsyncSession = Depends(get_async_session)
):
    await AdsORM.insert_ad(
        ad=ad_data,
        user_id=user_id,
        session=db_session
    )
    return CreatedResponse()

