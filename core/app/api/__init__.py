#маршрутизация эндпоинтов

from fastapi import FastAPI

from app.api.routers.auth import router as auth_router
from app.api.routers.shoes import router as shoes_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(shoes_router, prefix="/api", tags=["Shoes"])
