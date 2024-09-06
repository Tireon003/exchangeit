from pydantic import BaseModel, PositiveInt, Field
from datetime import datetime as dt

from models import UserTable, CategoryTable


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
    created_at: dt

    class Config:
        from_attributes = True


class AdDBRelBelongsto(AdFromDB):
    belongs_to: "UserTable"


class AdDBRelInFavorites(AdFromDB):
    in_user_favorites: list["UserTable"]


class AdDBRelCategory(AdFromDB):
    ad_category: "CategoryTable"
