from core import database as db
from models import AdTable, FavoriteTable
from schemas import AdFromDB, AdCreate

from sqlalchemy import select, and_


class AdsORM:

    @staticmethod
    async def search_ads_order_by_public_date() -> list[AdTable] | None:
        async with db.create_async_session() as session:
            query = select(AdTable).order_by(AdTable.created_at)
            result = await session.scalars(query)
            ads_by_date = [AdFromDB.model_validate(row) for row in result.all()]
            return ads_by_date

    @staticmethod
    async def search_ads_by_item_give(item_name: str) -> list[AdTable] | None:
        async with db.create_async_session() as session:
            query = select(AdTable).where(AdTable.item_give.like(f"%{item_name}%"))
            result = await session.scalars(query)
            ads_by_item_give = [AdFromDB.model_validate(row) for row in result.all()]
            return ads_by_item_give

    @staticmethod
    async def search_ads_by_item_get(item_name: str) -> list[AdTable] | None:
        async with db.create_async_session() as session:
            query = select(AdTable).where(AdTable.item_get.like(f"%{item_name}%"))
            result = await session.scalars(query)
            ads_by_item_get = [AdFromDB.model_validate(row) for row in result.all()]
            return ads_by_item_get

    @staticmethod
    async def search_ads_give_get(item_give: str, item_get: str) -> list[AdTable] | None:
        async with db.create_async_session() as session:
            query = select(AdTable).where(and_(AdTable.item_give.like(f"%{item_give}%"),
                                               AdTable.item_get.like(f"%{item_get}%")))
            result = await session.scalars(query)
            ads_give_get = [AdFromDB.model_validate(row) for row in result.all()]
            return ads_give_get

    @staticmethod
    async def select_user_ads(user_id: int) -> list[AdTable] | None:
        async with db.create_async_session() as session:
            query = select(AdTable).filter_by(id=user_id)
            result = await session.scalars(query)
            user_ads = [AdFromDB.model_validate(ad) for ad in result.all()]
            return user_ads

    @staticmethod
    async def select_favorite_list(user_id: int) -> list[AdTable] | None:
        async with db.create_async_session() as session:
            query = select(FavoriteTable).filter_by(user_id=user_id)
            result = await session.scalars(query)
            favorite_list = [AdFromDB.model_validate(ad) for ad in result.all()]
            return favorite_list

    @staticmethod
    async def insert_ad(ad: AdCreate, user_id: int):
        async with db.create_async_session() as session:
            ad_dict = ad.model_dump()
            ad_dict.update({"by_user": user_id})
            session.add(AdTable(**ad_dict))
            await session.commit()
