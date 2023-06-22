from fastapi import APIRouter, Depends, HTTPException, Form

from models.schemas.user_schemas import UserRegisterSchema, User
from .jwt import create_access_token
from core.storage.user_storage import UserStorage

# Ouath2
router = APIRouter(prefix='/api/auth', tags=['Auth'])


@router.post("/token")
async def login(phone: str = Form(alias='username'), password: str = Form()):
    user = await UserStorage.get_user_via_phone_number(phone)
    user = await UserStorage.login_user(user, password)

    # Генерация access токена
    access_token = create_access_token(data={"sub": user.phone, "authType": "website"})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/sign-up', response_model=User)
async def register_user(user: UserRegisterSchema):
    return await UserStorage.create_user(user)
