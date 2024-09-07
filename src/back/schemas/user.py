from pydantic import BaseModel, Field, PositiveInt
from datetime import datetime as dt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas import AdFromDB, ContactCardFromDB


class User(BaseModel):
    username: str = Field(max_length=20)
    hashed_password: str


class UserCreate(User):
    pass


class UserLogin(User):
    pass


class UserUpdate(User):
    pass


class UserFromDB(User):
    id: PositiveInt
    signup_timestamp: dt
    last_activity: dt
    is_active: bool

    class Config:
        from_attributes = True


class UserDBRelFavAds(UserFromDB):
    favorite_ads: "AdFromDB"


class UserDBRelAds(UserFromDB):
    user_ads: list["AdFromDB"]


class UserDBRelContacts(UserFromDB):
    contacts: "ContactCardFromDB"
