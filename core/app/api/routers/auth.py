from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.auth.jwt import create_access_token, get_current_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


@router.post("/token")
async def login(username: str, password: str):
    # Здесь должна быть ваша логика проверки учетных данных (например, валидация пользователя в базе данных)
    # В данном примере проверяем пароль "password" для примера
    if password != "password":
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Генерация access токена
    access_token = create_access_token(data={"sub": username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    # В этом эндпоинте вы можете разместить защищенную функциональность, к которой имеют доступ только аутентифицированные пользователи
    return {"message": "Protected route", "user": current_user}
