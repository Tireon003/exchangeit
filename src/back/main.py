import uvicorn
from contextlib import asynccontextmanager
from redis import asyncio as aioredis
from fastapi import FastAPI, Body, Path, status
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from orm import AdsORM, ContactORM
from schemas import AdFromDB, SearchData
from routes import auth_router, users_router, ads_router

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --------Startup-------
    redis = await aioredis.from_url(
        url="redis://redis:6379",
        encoding="utf-8",
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
    # ----------------------

    yield

    # ------Shutdown--------
    await redis.close()
    # ----------------------


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(ads_router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
