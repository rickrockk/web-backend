# Данный файл служит для генерации и валидации JWT токенов

from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

# from fastapi.security import OAuth2PasswordBearer
# from .jwt import decode_access_token
from config import Config


SECRET_KEY = Config.secret  # Секретный ключ для подписи JWT
ALGORITHM = "HS256"  # Алгоритм шифрования
ACCESS_TOKEN_EXPIRE_MINUTES = Config.token_lifetime  # Время жизни access токена

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Генерация хеша пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Генерация JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Декодирование JWT токена
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# TODO перенести в DAL
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = decode_access_token(token)
#         username = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
#         # TODO Здесь может быть ваша логика получения пользователя из базы данных или другого хранилища по имени пользователя (username)
#         #     Пример:
#         #     user = get_user_by_username(username)
#         #     if user is None:
#         #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
#         #     return user
#         #     В данном примере просто возвращаем имя пользователя
#         return username
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
