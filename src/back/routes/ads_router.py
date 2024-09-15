from fastapi import APIRouter, Depends, status, Body, Path
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_async_session
from schemas import AdFromDB, SearchData, ContactCardFromDB
from orm import AdsORM, ContactORM


router = APIRouter(
    prefix="/api/ads",
    tags=["ads"],
)


@router.post("/", response_model=list[AdFromDB | None], status_code=status.HTTP_200_OK)
async def get_ads(
        search_result: Annotated[SearchData, Body()],
        db_session: AsyncSession = Depends(get_async_session)
):
    if len(search_result.item_get) and len(search_result.item_give):
        ads = await AdsORM.search_ads_give_get(
            item_get=search_result.item_get,
            item_give=search_result.item_give,
            session=db_session,
        )
    elif len(search_result.item_get):
        ads = await AdsORM.search_ads_by_item_get(
            item_name=search_result.item_get,
            session=db_session,
        )
    elif len(search_result.item_give):
        ads = await AdsORM.search_ads_by_item_give(
            item_name=search_result.item_give,
            session=db_session,
        )
    else:
        ads = await AdsORM.search_ads_order_by_public_date(session=db_session)
    return ads if ads else []


@router.get("/{ad_id}/contact", response_model=ContactCardFromDB)
async def get_contact_from_ad(
        ad_id: Annotated[int, Path()],
        db_session: AsyncSession = Depends(get_async_session)
):
    contacts_card_model = await ContactORM.get_contact_from_ad(ad_id, db_session)
    return contacts_card_model
