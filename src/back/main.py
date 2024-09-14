import uvicorn
from contextlib import asynccontextmanager
from redis import asyncio as aioredis
from fastapi import FastAPI, Body, Path, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from orm import UserORM, AdsORM, ContactORM
from schemas import UserCreate, AdCreate, AdFromDB, SearchData, UserFromDB

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup

    redis = await aioredis.from_url(
        url="redis://redis:6379",
        encoding="utf-8",  # по дефолту такое же значение
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix="fastapi-cache",
    )

    try:
        await redis.ping()
        print("Connected to Redis successfully")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")

    yield

    # Shutdown
    await redis.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users/new_user")
async def create_user(user_data: Annotated[UserCreate, Body()]):
    founded_user = await UserORM.select_user_by_username(user_data.username)
    if not founded_user:
        await UserORM.create_user(user_data)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "User created",
            },
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_data.username} already exists",
        )


@app.get("/users/{user_id}", response_model=UserFromDB, status_code=status.HTTP_200_OK)
async def get_user(user_id: Annotated[int, Path()]):
    user = await UserORM.select_user_by_id(user_id)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"info": f"User with id {user_id} not found"},
        )


@app.post("/ads", response_model=list[AdFromDB] | None, status_code=status.HTTP_200_OK)
async def get_ads(search_result: Annotated[SearchData, Body()]):
    if len(search_result.item_get) and len(search_result.item_give):
        ads = await AdsORM.search_ads_give_get(
            item_get=search_result.item_get,
            item_give=search_result.item_give,
        )
    elif len(search_result.item_get):
        ads = await AdsORM.search_ads_by_item_get(search_result.item_get)
    elif len(search_result.item_give):
        ads = await AdsORM.search_ads_by_item_give(search_result.item_give)
    else:
        ads = await AdsORM.search_ads_order_by_public_date()
    return ads if ads else []


@app.post("/users/{user_id}/ads/new")
async def create_ad(ad_data: Annotated[AdCreate, Body()], user_id: Annotated[int, Path()]):
    await AdsORM.insert_ad(ad_data, user_id)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"msg": "successful"}
    )


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
