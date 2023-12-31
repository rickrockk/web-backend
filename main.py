import threading
from datetime import datetime, timezone

import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware


from config import Config
from loguru import logger
from database import connect_database
from config import Config
# routers
from fastapi import BackgroundTasks
from core.auth.auth import router as auth_router
from core.shoes_handlers.shoes import router as shoes_router
from core.vk_auth.vk_auth import router as vk_auth_router
from core.tasks.db_dump import DatabaseDump
from core.history_logger.middleware import user_history_middleware

# Dumps
db_dump = DatabaseDump()
dump_thread = threading.Thread(target=db_dump.run_pending)
dump_thread.daemon = True
dump_thread.start()


app = FastAPI()

# Including routers
app.include_router(auth_router)
app.include_router(shoes_router)
app.include_router(vk_auth_router)
app.add_middleware(BaseHTTPMiddleware, dispatch=user_history_middleware)


@app.on_event('startup')
async def on_startup():
    await connect_database()
    logger.success('Application startup complete at {time}', time=datetime.now(tz=timezone.utc))


if __name__ == '__main__':
    uvicorn.run('main:app', host=str(Config.host), port=Config.port, reload=True)
