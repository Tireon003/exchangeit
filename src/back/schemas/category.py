from pydantic import BaseModel, Field, PositiveInt

from models import AdTable


class Category(BaseModel):
    category_name: str = Field(max_length=40)


class CategoryCreate(Category):
    pass


class CategoryFromDB(Category):
    id: PositiveInt

    class Config:
        from_attributes = True


class CategoryDBRelAds(CategoryFromDB):
    ads_in_category: list["AdTable"]
