from fastapi import APIRouter, Depends, HTTPException, Form, BackgroundTasks

from models.schemas.user_schemas import UserRegisterSchema, User
from .jwt import create_access_token
from core.storage.user_storage import UserStorage
from core.tasks.send_mail import send_mail

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
async def register_user(user: UserRegisterSchema, background_tasks: BackgroundTasks):
    user = await UserStorage.create_user(user)
    background_tasks.add_task(send_mail, text="You have been singed up at crossowker", me="no-reply@crossowker.ru",
                              to=user.email, subject="Activate your account")
    return user
