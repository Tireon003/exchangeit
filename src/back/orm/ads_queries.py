from models import AdTable, FavoriteTable, AdsContactsTable
from schemas import AdFromDB, AdCreate
from sqlalchemy.ext.asyncio import AsyncSession

from .contact_queries import ContactORM

from sqlalchemy import select, and_, func
from fastapi_cache.decorator import cache


class AdsORM:

    @staticmethod
    @cache(expire=60)
    async def search_ads_order_by_public_date(session: AsyncSession) -> list[AdFromDB] | None:
        query = select(AdTable).order_by(AdTable.created_at)
        result = await session.scalars(query)
        ads_by_date = [AdFromDB.model_validate(row) for row in result.all()]
        return ads_by_date

    @staticmethod
    @cache(expire=60)
    async def search_ads_by_item_give(item_name: str, session: AsyncSession) -> list[AdFromDB] | None:
        query = (
            select(AdTable)
            .where(
                func.lower(AdTable.item_give).like(f"%{item_name.casefold()}%")
            )
        )
        result = await session.scalars(query)
        ads_by_item_give = [AdFromDB.model_validate(row) for row in result.all()]
        return ads_by_item_give

    @staticmethod
    @cache(expire=60)
    async def search_ads_by_item_get(item_name: str, session: AsyncSession) -> list[AdFromDB] | None:
        query = (
            select(AdTable)
            .where(
                func.lower(AdTable.item_get).like(f"%{item_name.casefold()}%")
            )
        )
        result = await session.scalars(query)
        ads_by_item_get = [AdFromDB.model_validate(row) for row in result.all()]
        return ads_by_item_get

    @staticmethod
    @cache(expire=60)
    async def search_ads_give_get(item_give: str, item_get: str, session: AsyncSession) -> list[AdFromDB] | None:
        query = (
            select(AdTable)
            .where(
                and_(
                    func.lower(AdTable.item_get).like(f"%{item_give.casefold()}%"),
                    func.lower(AdTable.item_get).like(f"%{item_get.casefold()}%")
                )
            )
        )
        result = await session.scalars(query)
        ads_give_get = [AdFromDB.model_validate(row) for row in result.all()]
        return ads_give_get

    @staticmethod
    async def select_user_ads(user_id: int, session: AsyncSession) -> list[AdFromDB] | None:
        query = select(AdTable).filter_by(id=user_id)
        result = await session.scalars(query)
        user_ads = [AdFromDB.model_validate(ad) for ad in result.all()]
        return user_ads

    @staticmethod
    async def select_favorite_list(user_id: int, session: AsyncSession) -> list[AdFromDB] | None:
        query = select(FavoriteTable).filter_by(user_id=user_id)
        result = await session.scalars(query)
        favorite_list = [AdFromDB.model_validate(ad) for ad in result.all()]
        return favorite_list

    @staticmethod
    async def insert_ad(ad: AdCreate, user_id: int, session: AsyncSession):
        contact_id = await ContactORM.get_contact_id_by_user_id(user_id, session)
        ad_dict = ad.model_dump()
        ad_dict.update({"by_user": user_id})
        ad_dto = AdTable(**ad_dict)
        session.add(ad_dto)
        await session.flush()
        await session.refresh(ad_dto)
        ad_contact_sec = AdsContactsTable(**{
            "ad_id": ad_dto.id,
            "contact_id": contact_id
        })
        session.add(ad_contact_sec)
        await session.commit()

    @staticmethod
    async def select_ad_by_id(ad_id: int, session: AsyncSession) -> list[AdFromDB] | None:
        query = select(AdTable).filter_by(id=ad_id)
        result = await session.scalars(query)
        ad = result.one_or_none()
        if ad:
            ad_model = AdFromDB.model_validate(ad)
            return ad_model
