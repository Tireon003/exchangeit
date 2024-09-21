import uvicorn
from contextlib import asynccontextmanager
from redis import asyncio as aioredis
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from routes import auth_router, users_router, ads_router
from exceptions import ExpiredTokenException, InvalidTokenException

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


@app.exception_handler(ExpiredTokenException)
async def handle_expired_token_exception(request: Request, exc: ExpiredTokenException):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Access token expired",
        headers={"WWW-Authenticate": "Bearer"}
    )


@app.exception_handler(InvalidTokenException)
async def handle_expired_token_exception(request: Request, exc: InvalidTokenException):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access token",
        headers={"WWW-Authenticate": "Bearer"}
    )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
