from core import database as db
from models import UserTable, AdTable

from sqlalchemy import select, and_


class Crud:

    @staticmethod
    async def create_user(username: str, hashed_password: str):
        async with db.create_async_session() as session:
            new_user = UserTable(
                username=username,
                hashed_password=hashed_password,
            )
            session.add(new_user)
            await session.commit()

    @staticmethod
    async def select_user(user_id: int):
        async with db.create_async_session() as session:
            user = await session.get(UserTable, user_id)
            return user

    @staticmethod
    async def update_user_password(user_id: int, hashed_password: str):
        async with db.create_async_session() as session:
            user = await session.get(UserTable, user_id)
            user.hashed_password = hashed_password
            await session.commit()

    @staticmethod
    async def delete_user(user_id: int):
        async with db.create_async_session() as session:
            user = await session.get(UserTable, user_id)

    @staticmethod
    async def search_ads_order_by_public_date() -> list[None | dict]:
        async with db.create_async_session() as session:
            query = select(AdTable).order_by(AdTable.created_at)
            result = await session.scalars(query)
            ads_by_date = [dict(row) for row in result.all()]
            return ads_by_date

    @staticmethod
    async def search_ads_by_item_give(item_name: str) -> list[None | dict]:
        async with db.create_async_session() as session:
            query = select(AdTable).where(AdTable.item_give.like(item_name))
            result = await session.scalars(query)
            ads_by_item_give = [dict(row) for row in result.all()]
            return ads_by_item_give

    @staticmethod
    async def search_ads_by_item_get(item_name: str) -> list[None | dict]:
        async with db.create_async_session() as session:
            query = select(AdTable).where(AdTable.item_get.like(item_name))
            result = await session.scalars(query)
            ads_by_item_get = [dict(row) for row in result.all()]
            return ads_by_item_get

    @staticmethod
    async def search_ads_give_get(item_give: str, item_get: str) -> list[None | dict]:
        async with db.create_async_session() as session:
            query = select(AdTable).where(and_(AdTable.item_give.like(item_give), AdTable.item_get.like(item_get)))
            result = await session.scalars(query)
            ads_give_get = [dict(row) for row in result.all()]
            return ads_give_get

