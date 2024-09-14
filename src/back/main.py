import uvicorn
from fastapi import FastAPI, Body, Path, HTTPException, status, Response
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated

from orm import UserORM, AdsORM, ContactORM
from schemas import UserCreate, AdCreate

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


@app.post("/users/new_user")
async def create_user(user_data: Annotated[UserCreate, Body()]):
    founded_user = await UserORM.select_user_by_username(user_data.username)
    if not founded_user:
        await UserORM.create_user(user_data)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "User created",
                "data": user_data.model_dump()
            },
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {user_data.username} already exists",
        )


@app.get("/ads", response_model=list[dict])
async def get_ads():
    ads = await AdsORM.search_ads_order_by_public_date()
    ads_json = []
    for item in ads:
        ad = item.model_dump()
        ad["created_at"] = item.created_at.isoformat()
        ads_json.append(ad)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ads_json,
    )


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
