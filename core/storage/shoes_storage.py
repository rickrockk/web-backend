from typing import Type

from .base_storage import BaseStorage
from fastapi import Depends, HTTPException
from ..auth.oauth_scheme import oauth2_scheme
from models.schemas.shoes_schemas import Item, ItemDetailSchema, Category, OptionSchema, ItemsListSchema, \
    ItemOptionCreateSchema
from sqlalchemy import Select, Insert, Update, Delete
from sqlalchemy.orm import join
from models.models import Item as ItemOrm, Categories as CategoryOrm, ItemSizeColorAvailability as OptionsOrm


class ItemStorage(BaseStorage):

    @classmethod
    async def retrieve_item(cls, query: Select | Insert | Update | Delete) -> Item:
        return await cls.retrieve_row(query, Item, error_msg="Item not found error")

    @classmethod
    async def retrieve_category(cls, query: Select | Insert | Update | Delete) -> Category:
        return await cls.retrieve_row(query, Category, error_msg='Category not found')

    @classmethod
    async def retrieve_option(cls, query: Select | Insert | Update | Delete) -> OptionSchema:
        return await cls.retrieve_row(query, OptionSchema, error_msg='Item options not found')

    @classmethod
    async def retrieve_category_via_id(cls, category_id: int):
        sql = Select(CategoryOrm).where(CategoryOrm.id == category_id)
        return await cls.retrieve_category(sql)

    @classmethod
    async def create_item(cls, item: ItemOptionCreateSchema) -> ItemDetailSchema:
        options = item.options

        sql = Insert(ItemOrm).values(**(item.item.dict(exclude_none=True))
                                     ).returning(ItemOrm)

        item_obj = await cls.retrieve_item(sql)

        options_data = []
        for opt in options:
            option = OptionSchema(part_number=opt.part_number,
                                  item_id=item_obj.id,
                                  size=opt.size,
                                  color=opt.color,
                                  price=opt.price,
                                  is_available=opt.is_available,
                                  images=opt.images
                                  )

            if len(option.images) == 0:
                option.images = None

            sql = Insert(OptionsOrm).values(**option.dict(exclude_none=True)).returning(OptionsOrm)
            options_data.append(await cls.retrieve_option(sql))

        return ItemDetailSchema(item=item_obj, options=options_data)

    @classmethod
    async def get_item_detail(cls, item_id: int) -> ItemDetailSchema:
        sql = Select(ItemOrm).where(ItemOrm.id == item_id)
        item = await cls.retrieve_item(sql)
        options_sql = Select(OptionsOrm).where(OptionsOrm.item_id == item_id)
        options = await cls.retrieve_many(options_sql, OptionSchema)
        return ItemDetailSchema(item=item, options=options)

    @classmethod
    async def list_items(cls, limit: int = 50, page: int = 0) -> list[ItemsListSchema]:
        sql = Select(
            ItemOrm.id.label('id'),
            ItemOrm.name.label('name'),
            ItemOrm.description.label('description'),
            CategoryOrm.name.label('category')
        ).select_from(join(ItemOrm, CategoryOrm, ItemOrm.category_id == CategoryOrm.id)).limit(limit).offset(
            page * limit)
        return await cls.retrieve_many(sql, ItemsListSchema)

    # @classmethod
    # async def get_item_via_name(cls, item_name: str):
    #     sql = Select(ItemOrm).where(ItemOrm.name == item_name)
    #     return await cls.retrieve_item(sql)
