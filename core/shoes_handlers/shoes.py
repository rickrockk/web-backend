from fastapi import APIRouter, Depends, HTTPException, Form, Path, BackgroundTasks
from fastapi_cache.decorator import cache

from models.schemas.shoes_schemas import Item, ItemDetailSchema, ItemsListSchema, ItemOptionCreateSchema, \
    CreateCategorySchema, Category, Size, Color

from models.schemas.user_schemas import User
from ..storage.shoes_storage import ItemStorage
from core.tasks.celery_worker import send_mail



router = APIRouter(prefix='/api', tags=['Shoes'])


@router.post('/shoes', response_model=ItemDetailSchema)
async def create_shoe(item: ItemOptionCreateSchema, user: User):
    return await ItemStorage.create_item(item)


@router.get('/shoes', response_model=list[ItemsListSchema])
@cache(expire=60)
async def list_items(items: list[ItemsListSchema] = Depends(ItemStorage.list_items)):
    send_mail.delay(me='hihihiha', to='azaza@mail.ru', text='azaza', subject='azaza')
    return items


@router.get("/shoes/{item_id}", response_model=ItemDetailSchema)
@cache(expire=60)
async def detail_shoe(item_id: int = Path()):
    return await ItemStorage.get_item_detail(item_id)


@router.post('/categories', response_model=Category)
async def create_category(category: CreateCategorySchema):
    return await ItemStorage.create_category(category)


@router.get('/categories', response_model=list[Category])
@cache(expire=60)
async def list_categories():
    return await ItemStorage.list_categories()


@router.post('/sizes', response_model=Size)
async def create_sizes(size: Size):
    return await ItemStorage.create_size(size)


@router.get('/sizes', response_model=list[Size])
@cache(expire=60)
async def list_sizes():
    return await ItemStorage.list_sizes()


@router.post('/colors', response_model=Color)
async def create_colors(color: Color):
    return ItemStorage.create_color(color)


@router.get('/colors', response_model=list[Color])
@cache(expire=60)
async def list_colors():
    return await ItemStorage.list_colors()

# @router.get("/{shoe_id}", response_model=ShoeResponse)
# async def get_shoe_by_id(shoe_id: int):
#     pass
#     # shoe = get_shoe(shoe_id)
#     # return shoe
#
#
# @router.post("/", response_model=ShoeResponse)
# async def add_shoe(shoe: ShoeCreate, token: str = Depends(decode_access_token)):
#     pass
#     # created_shoe = create_shoe(shoe)
#     # return created_shoe
#
#
# @router.put("/{shoe_id}", response_model=ShoeResponse)
# async def update_shoe_by_id(shoe_id: int, shoe: ShoeUpdate, token: str = Depends(decode_access_token)):
#     pass
#     # updated_shoe = update_shoe(shoe_id, shoe)
#     # return updated_shoe
#
#
# @router.delete("/shoe_id}")
# async def delete_shoe_by_id(shoe_id: int, token: str = Depends(decode_access_token)):
#     pass
#     # delete_shoe(shoe_id)
#     # return {"message": "Shoe deleted successfully"}
