from fastapi import Request, Header
import json
from sqlalchemy import Select, Insert
from models.models import UserHistory
from datetime import datetime
from database import database


async def user_history_middleware(request: Request, call_next):
    url = request.url
    sql = Insert(UserHistory).values(timestamp=datetime.now(), url=str(url.path), user_agent=json.dumps(dict(request.headers)))
    await database.execute(sql)

    response = await call_next(request)
    return response
