from pydantic import BaseModel, Field, PositiveInt, PlainSerializer
from datetime import datetime as dt
from typing import TYPE_CHECKING, Annotated

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
    signup_timestamp: Annotated[dt, PlainSerializer(
        lambda val: val.strftime(format="%Y-%m-%d %H:%M:%S"),
        return_type=str)
    ]
    last_activity: Annotated[dt, PlainSerializer(
        lambda val: val.strftime(format="%Y-%m-%d %H:%M:%S"),
        return_type=str)
    ]
    is_active: bool

    class Config:
        from_attributes = True


class UserDBRelFavAds(UserFromDB):
    favorite_ads: "AdFromDB"


class UserDBRelAds(UserFromDB):
    user_ads: list["AdFromDB"]


class UserDBRelContacts(UserFromDB):
    contacts: "ContactCardFromDB"
