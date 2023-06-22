from fastapi import APIRouter, Depends


# TODO А где эти модели ?
# from app.api.models import ShoeCreate, ShoeUpdate, ShoeResponse
# from app.core.auth.jwt import decode_access_token
# from app.core.services.shoes import create_shoe, get_all_shoes, get_shoe, update_shoe, delete_shoe

router = APIRouter(prefix='api/shoes')


@router.get("/", response_model=list[ShoeResponse])
async def get_shoes():
    shoes = get_all_shoes()
    return shoes


@router.get("/{shoe_id}", response_model=ShoeResponse)
async def get_shoe_by_id(shoe_id: int):
    shoe = get_shoe(shoe_id)
    return shoe


@router.post("/", response_model=ShoeResponse)
async def add_shoe(shoe: ShoeCreate, token: str = Depends(decode_access_token)):
    created_shoe = create_shoe(shoe)
    return created_shoe


@router.put("/{shoe_id}", response_model=ShoeResponse)
async def update_shoe_by_id(shoe_id: int, shoe: ShoeUpdate, token: str = Depends(decode_access_token)):
    updated_shoe = update_shoe(shoe_id, shoe)
    return updated_shoe


@router.delete("/shoe_id}")
async def delete_shoe_by_id(shoe_id: int, token: str = Depends(decode_access_token)):
    delete_shoe(shoe_id)
    return {"message": "Shoe deleted successfully"}
