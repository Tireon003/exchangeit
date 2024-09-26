from fastapi import (
    APIRouter,
    Depends,
    status,
    Body,
    Query,
    HTTPException,
)
from fastapi.responses import JSONResponse
from typing import Annotated

from core import database as db
from ad.schemas import AdCreate, AdFromDB
from auth.depends import validate_token
from auth.schemas import AccessTokenPayload

from .depends import get_user_repository
from .repository import UserRepository
from .schemas import UserDBRelsAdsFavContacts
from .exceptions import UserNotFoundException, AdAlreadyInFavoritesException


router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.get(path="/me",
            response_model=UserDBRelsAdsFavContacts,
            status_code=status.HTTP_200_OK,
            description="Get user info")
async def get_user_data_full(
        token_payload: Annotated[AccessTokenPayload, Depends(validate_token)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository(db.get_async_session))]
):
    user_data_full = await user_repository.get_user(user_id=token_payload.usr)
    if not user_data_full:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {token_payload.usr} not found",
        )
    else:
        user_dto = UserDBRelsAdsFavContacts.model_validate(user_data_full)
        return user_dto


@router.post("/me/ads/new")
async def create_ad(
        ad_data: Annotated[AdCreate, Body()],
        token_payload: Annotated[AccessTokenPayload, Depends(validate_token)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository(db.get_async_session))]
):
    ad_id = await user_repository.create_ad(
        user_id=token_payload.usr,
        ad=ad_data
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        media_type="application/json",
        content={
            "msg": "Ad successfully created",
            "id": ad_id
        }
    )


@router.get(path="/me/wishlist",
            response_model=list[AdFromDB] | None,
            status_code=status.HTTP_200_OK,
            description="Get user wishlist")
async def get_user_wishlist(
        token_payload: Annotated[AccessTokenPayload, Depends(validate_token)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository(db.get_async_session))]
):
    try:
        wishlist = await user_repository.get_favorite_ads(user_id=token_payload.usr)
        return wishlist
    except UserNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {exc.user_id} not found",
        )


@router.post(path="/me/wishlist",
             description="Add ad to user wishlist")
async def add_ad_to_user_wishlist(
        ad_id: Annotated[int, Query()],
        token_payload: Annotated[AccessTokenPayload, Depends(validate_token)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository(db.get_async_session))]
):
    try:
        await user_repository.insert_ad_to_favorite(
            user_id=token_payload.usr,
            ad_id=ad_id
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            media_type="application/json",
            content={
                "msg": "Ad successfully added to user wishlist",
                "id": ad_id,
            }
        )
    except UserNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {exc.user_id} not found",
        )
    except AdAlreadyInFavoritesException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ad with id {exc.ad_id} already in favorites"
        )


@router.delete(path="/me/wishlist",
               description="Remove ad from user wishlist")
async def remove_ad_from_wishlist(
        ad_id: Annotated[int, Query()],
        token_payload: Annotated[AccessTokenPayload, Depends(validate_token)],
        user_repository: Annotated[UserRepository, Depends(get_user_repository(db.get_async_session))]
):
    await user_repository.remove_ad_from_favorite(
        user_id=token_payload.usr,
        ad_id=ad_id
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        media_type="application/json",
        content={
            "msg": "Ad successfully removed from user wishlist",
            "id": ad_id,
        }
    )
