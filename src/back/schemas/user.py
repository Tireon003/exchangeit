from pydantic import BaseModel, Field, PositiveInt, PlainSerializer
from datetime import datetime as dt
from typing import TYPE_CHECKING, Annotated


from .ad import AdFromDB
from .contacts import ContactCardFromDB


class User(BaseModel):
    username: str = Field(max_length=20)
    hashed_password: str


class UserCreate(User):
    pass


class UserLogin(User):
    pass


class UserCreds(BaseModel):
    username: str = Field(max_length=20)
    password: str = Field(min_length=8)


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
    favorite_ads: list["AdFromDB"]


class UserDBRelAds(UserFromDB):
    user_ads: list["AdFromDB"]


class UserDBRelContacts(UserFromDB):
    contacts: "ContactCardFromDB"


class UserDBRelsAdsFavContacts(UserDBRelFavAds, UserDBRelAds, UserDBRelContacts):
    pass
