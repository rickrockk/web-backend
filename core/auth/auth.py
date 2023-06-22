from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from .jwt import create_access_token

# Ouath2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
router = APIRouter(prefix='/api/auth')


# TODO Поменять на multipart form data
@router.post("/token")
async def login(username: str = Form(), password: str = Form()):
    # TODO make Storage service with loging user
    #   Здесь должна быть ваша логика проверки учетных данных (например, валидация пользователя в базе данных)
    #   В данном примере проверяем пароль "password" для примера
    #    if password != "password":
    #       raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Генерация access токена
    access_token = create_access_token(data={"sub": username})

    return {"access_token": access_token, "token_type": "bearer"}
