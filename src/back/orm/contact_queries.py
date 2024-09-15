from models import AdTable, ContactTable
from schemas import ContactCardFromDB

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class ContactORM:

    @staticmethod
    async def get_contact_from_ad(ad_id: int, session: AsyncSession) -> ContactCardFromDB:
        get_contact_from_ad_query = select(AdTable). \
                                    options(joinedload(AdTable.ad_contacts)). \
                                    filter_by(id=ad_id)
        result = await session.scalars(get_contact_from_ad_query)
        ad_item = result.one_or_none()
        if not ad_item:
            return
        contact_model = ContactCardFromDB.model_validate(ad_item.ad_contacts)
        return contact_model

    @staticmethod
    async def get_contact_id_by_user_id(user_id: int, session: AsyncSession) -> int | None:
        query = select(ContactTable).filter_by(by_user=user_id)
        result = await session.scalars(query)
        contacts = result.one_or_none()
        return contacts.id if contacts else None

