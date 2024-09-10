from pydantic import BaseModel


class AdsContacts(BaseModel):
    ad_id: int
    contact_id: int


class AdsContactsFromDB(AdsContacts):

    class Config:
        from_attributes = True