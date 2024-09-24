from fastapi import APIRouter, Depends, status, Body, Path
from typing import Annotated

from core import database as db

from contact.schemas import ContactCardFromDB

from .repository import AdsRepository
from .depends import get_ads_repository
from .schemas import SearchData, AdFromDB


router = APIRouter(
    prefix="/api/ads",
    tags=["ads"],
)


@router.post("/", response_model=list[AdFromDB] | None, status_code=status.HTTP_200_OK)
async def get_ads(
        search_result: Annotated[SearchData, Body()],
        ad_repository: Annotated[AdsRepository, Depends(get_ads_repository(db.get_async_session))]
):
    ads = await ad_repository.search_ads(
        item_give=search_result.item_give,
        item_get=search_result.item_get
    )
    ads_dto = [AdFromDB.model_validate(ad) for ad in ads]
    return ads_dto


@router.get("/{ad_id}/contact", response_model=ContactCardFromDB, status_code=status.HTTP_200_OK)
async def get_contact_from_ad(
        ad_id: Annotated[int, Path()],
        ad_repository: Annotated[AdsRepository, Depends(get_ads_repository(db.get_async_session))]
):
    contacts = await ad_repository.get_contact_from_ad(ad_id=ad_id)
    contacts_dto = ContactCardFromDB.model_validate(contacts)
    return contacts_dto
