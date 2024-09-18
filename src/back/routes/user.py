from fastapi import (
    APIRouter,
    Depends,
    Path,
    status,
    Body,
    HTTPException,
)

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_async_session, validate_token
from schemas import UserFromDB, AdCreate, CreatedResponse, AccessTokenPayload
from orm import UserORM, AdsORM

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
        token_payload: Annotated[AccessTokenPayload, Depends(validate_token)],
        db_session: AsyncSession = Depends(get_async_session)
):

    if user_id != token_payload.usr:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User id in path does not match token user id"
        )
    else:
        await AdsORM.insert_ad(
            ad=ad_data,
            user_id=user_id,
            session=db_session
        )
        return CreatedResponse()
