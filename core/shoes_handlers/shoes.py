from fastapi import APIRouter, Depends

from models.schemas.user_schemas import User
from ..storage.user_storage import UserStorage

# TODO А где эти модели ?
# from app.api.models import ShoeCreate, ShoeUpdate, ShoeResponse
# from app.core.auth.jwt import decode_access_token
# from app.core.services.shoes import create_shoe, get_all_shoes, get_shoe, update_shoe, delete_shoe
# from core.auth.auth import oauth2_scheme

router = APIRouter(prefix='/api/shoes', tags=['Shoes'])


@router.get("/")
async def get_shoes():
    user = User(name='ernest', phone='79024866500', email='ernest@el.tech', password="1234")
    print(await UserStorage.create_user(user))
    return 'ok'
    pass
    # shoes = get_all_shoes()
    # return shoes
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
