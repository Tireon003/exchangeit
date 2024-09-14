from pydantic import BaseModel, Field


class SearchData(BaseModel):
    item_get: str = Field(alias="itemGet")
    item_give: str = Field(alias="itemGive")

    class Config:
        populate_by_name = True
