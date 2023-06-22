from .base_storage import BaseStorage
from fastapi import Depends, HTTPException
from ..auth.oauth_scheme import oauth2_scheme
from models.schemas.user_schemas import Item, ItemCreateSchema
from sqlalchemy import Select, Insert, Update, Delete
from models.models import Item as ItemOrm


class ItemStorage(BaseStorage):

    @classmethod 
    async def retrieve_item(cls, query: Select | Insert | Update | Delete) -> Item:
        item_raw = await cls.db.fetch_row(query)
        if item_raw is None:
            raise HTTPException(status_code=400, detail="Item not found error")
        return Item.parse_obj(item_raw)
    
    @classmethod
    async def create_item(cls, item: ItemCreateSchema) -> Item:
        item.name = item.name
        item.description = item.description
        sql = Insert(ItemOrm).values(**item.dict(exclude_none=True)).returning(ItemOrm)
        return await cls.retrieve_item(sql)
    

    @classmethod
    async def get_item_via_id(cls, item_id: int):
        sql = Select(ItemOrm).where(ItemOrm.id == item_id)
        return await cls.retrieve_item(sql)

    @classmethod
    async def get_item_via_name(cls, item_name: str(50)):
        sql = Select(ItemOrm).where(ItemOrm.name == item_name)
        return await cls.retrieve_item(sql)
