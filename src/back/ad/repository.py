from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi_cache.decorator import cache

from models import AdTable, ContactTable

# todo add redis cache
class AdsRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def __repr__(self) -> str:
        """
        Overriding __repr__ for fastapi-cache
        :return:
        """
        return self.__class__.__name__

    @cache(expire=30)
    async def search_ads(self,
                         item_give: str = "",
                         item_get: str = "") -> list[AdTable] | None:
        stmt = select(AdTable)
        if item_get and item_give:
            stmt = stmt.where(
                and_(
                    func.lower(AdTable.item_give).like(f"%{item_give.casefold()}%"),
                    func.lower(AdTable.item_get).like(f"%{item_get.casefold()}%")
                )
            )
        elif item_give:
            stmt = stmt.where(func.lower(AdTable.item_give).like(f"%{item_give.casefold()}%"))
        elif item_get:
            stmt = stmt.where(func.lower(AdTable.item_get).like(f"%{item_get.casefold()}%"))
        result = await self.session.scalars(stmt)
        ads = result.all()
        return ads

    @cache(expire=30)
    async def get_contact_from_ad(self, ad_id: int) -> ContactTable | None:
        stmt = (
            select(AdTable)
            .options(joinedload(AdTable.ad_contacts))
            .filter_by(id=ad_id)
        )
        result = await self.session.scalars(stmt)
        ad = result.one_or_none()
        ad_contacts = ad.ad_contacts
        return ad_contacts
