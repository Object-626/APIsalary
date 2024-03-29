from fastapi import FastAPI
from app.users.routes import router as user_router
from app.auth.auth import router as auth_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

app = FastAPI(
    title="Зарплата сотрудников"
)
app.include_router(user_router)
app.include_router(auth_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
