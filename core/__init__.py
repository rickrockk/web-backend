from fastapi import FastAPI

from app.core.auth.jwt import get_password_hash

app = FastAPI()


# Инициализация компонентов авторизации
@app.on_event("startup")
async def startup():
    # Здесь можно добавить логику загрузки секретного ключа и других настроек авторизации
    # В данном примере просто прописываем хеш пароля для примера
    hashed_password = get_password_hash("password")  # Замените на фактический пароль
    # Далее можно сохранить хеш пароля в базе данных или в другом хранилище для будущей проверки
