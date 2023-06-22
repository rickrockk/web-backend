from fastapi import APIRouter, Depends, HTTPException, Form

from models.schemas.shoes_schemas import Item, ItemDetailSchema
from ..storage.shoes_storage import ItemStorage


router = APIRouter(prefix='/api/shoes', tags=['Shoes'])


@router.post('/create-shoe', response_model=Item)
async def create_shoe(item: ItemDetailSchema):
    return await ItemStorage.create_item(item)

@router.get("/{item_id}", response_model=ItemDetailSchema)
async def detail_shoe(item: ItemDetailSchema):
    return await ItemStorage.get_item_detail(item)
#
#
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
