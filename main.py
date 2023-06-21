from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI
from config import Config
from loguru import logger
from database import connect_database

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await connect_database()
    logger.success('Application startup complete at {time}', time=datetime.now(tz=timezone.utc))


if __name__ == '__main__':
    uvicorn.run('main:app', host=str(Config.host), port=Config.port, reload=True)
