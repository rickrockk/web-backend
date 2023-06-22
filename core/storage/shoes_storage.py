from typing import Type

from .base_storage import BaseStorage
from fastapi import Depends, HTTPException
from ..auth.oauth_scheme import oauth2_scheme
from models.schemas.shoes_schemas import Item, ItemCreateSchema, Category, ItemsColorSizeAvailability, \
    ItemCreateResponseSchema
from sqlalchemy import Select, Insert, Update, Delete
from models.models import Item as ItemOrm, Categories as CategoryOrm, ItemSizeColorAvailability as OptionsOrm


class ItemStorage(BaseStorage):

    @classmethod
    async def retrieve_item(cls, query: Select | Insert | Update | Delete) -> Item:
        return await cls.retrieve_row(query, Item, error_msg="Item not found error")

    @classmethod
    async def retrieve_category(cls, query: Select | Insert | Update | Delete) -> Category:
        return await cls.retrieve_row(query, Category, error_msg='Category not found')

    @classmethod
    async def retrieve_option(cls, query: Select | Insert | Update | Delete) -> ItemsColorSizeAvailability:
        return await cls.retrieve_row(query, ItemsColorSizeAvailability, error_msg='Item options not found')

    @classmethod
    async def retrieve_category_via_id(cls, category_id: int):
        sql = Select(CategoryOrm).where(CategoryOrm.id == category_id)
        return await cls.retrieve_category(sql)

    @classmethod
    async def create_item(cls, item: ItemCreateSchema) -> ItemCreateResponseSchema:
        options = item.options

        sql = Insert(ItemOrm).values(**(item.item.dict(exclude_none=True))
        ).returning(ItemOrm)

        item.item = await cls.retrieve_item(sql)

        options_data = []
        for opt in options:
            sql = Insert(OptionsOrm).values(opt.dict(exclude_none=True))
            options_data.append(await cls.retrieve_option(sql))

        item.options = options_data
        return Item

    @classmethod
    async def get_item_via_id(cls, item_id: int):
        sql = Select(ItemOrm).where(ItemOrm.id == item_id)
        return await cls.retrieve_item(sql)

    @classmethod
    async def get_item_via_name(cls, item_name: str):
        sql = Select(ItemOrm).where(ItemOrm.name == item_name)
        return await cls.retrieve_item(sql)
