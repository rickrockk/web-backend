from typing import TypeVar, Type
from sqlalchemy import Select, Insert, Update, Delete
from database import database
from pydantic import BaseModel, parse_obj_as
from fastapi import HTTPException

T = TypeVar("T")
SQL = TypeVar("SQL", Select, Insert, Update, Delete)


class BaseStorage:
    db = database

    @classmethod
    async def retrieve_row(cls, query: SQL, response_model: T, error_msg: str = None) -> Type[T]:
        if error_msg is None:
            error_msg = 'Not found'

        item_raw = await cls.db.fetch_row(query)
        if item_raw is None:
            raise HTTPException(status_code=400, detail=error_msg)
        return response_model.parse_obj(item_raw)

    @classmethod
    async def retrieve_many(cls, query: SQL, response_model: Type[T], error_msg: str = None) -> list[Type[T]]:
        if error_msg is None:
            error_msg = "Not found"
        items = await cls.db.fetch(query)

        return parse_obj_as(list[response_model], items)
