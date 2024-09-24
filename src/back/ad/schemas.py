from pydantic import BaseModel, PositiveInt, Field, PlainSerializer
from datetime import datetime as dt
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from contact.schemas import ContactCardFromDB
    from user.schemas import UserFromDB


class Ad(BaseModel):
    category: PositiveInt
    item_give: str = Field(max_length=40)
    item_get: str = Field(max_length=40)
    description: str = Field(max_length=300)
    location: str = Field(max_length=80)


class AdCreate(Ad):
    pass


class AdUpdate(Ad):
    pass


class AdFromDB(Ad):
    id: PositiveInt
    by_user: PositiveInt
    created_at: Annotated[dt, PlainSerializer(lambda val: val.strftime(format="%Y-%m-%d %H:%M:%S"), return_type=str)]

    class Config:
        from_attributes = True


class AdDBRelBelongsto(AdFromDB):
    belongs_to: "UserFromDB"


class AdDBRelInFavorites(AdFromDB):
    in_user_favorites: list["UserFromDB"]


class AdDBRelCategory(AdFromDB):
    ad_category: "ContactCardFromDB"


class SearchData(BaseModel):
    item_give: str = Field(alias="itemGive")
    item_get: str = Field(alias="itemGet")

    class Config:
        populate_by_name = True
