from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from config import Config
from loguru import logger
from database import connect_database

# routers
from core.auth.auth import router as auth_router
from core.shoes_handlers.shoes import router as shoes_router
from core.vk_auth.vk_auth import router as vk_auth_router
app = FastAPI()

# Including routers
app.include_router(auth_router)
app.include_router(shoes_router)
app.include_router(vk_auth_router)


@app.on_event('startup')
async def on_startup():
    await connect_database()
    logger.success('Application startup complete at {time}', time=datetime.now(tz=timezone.utc))


if __name__ == '__main__':
    uvicorn.run('main:app', host=str(Config.host), port=Config.port, reload=True)
