import uvicorn
from fastapi import FastAPI, Body, Path, HTTPException, status
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated

from orm import UserORM, AdsORM, ContactORM
from schemas import UserCreate

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    response = list()
    response.append(await AdsORM.search_ads_order_by_public_date())
    response.append(await AdsORM.search_ads_by_item_give("some item"))
    response.append(await AdsORM.search_ads_by_item_get("another item"))
    response.append(await AdsORM.search_ads_give_get("yet another item", "other item"))
    return {
        "message": response,
        "status": "200 OK",
    }


@app.post("/create_user")
async def create_user(user_data: Annotated[UserCreate, Body()]):
    founded_user = await UserORM.select_user_by_username(user_data.username)
    if not founded_user:
        await UserORM.create_user(user_data)
        return {
            "message": "User created",
            "data": user_data.model_dump()
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_data.username} already exists",
        )


@app.get("/ads")
async def get_ads():
    ads = await AdsORM.search_ads_order_by_public_date()
    return ads


@app.get("/ads/{ad_id}/contact")
async def get_contact_from_ad(ad_id: Annotated[int, Path()]):
    contacts_model = await ContactORM.get_contact_from_ad(ad_id)
    return contacts_model


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
