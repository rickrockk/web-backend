from .base_storage import BaseStorage
from fastapi import Depends, HTTPException
from ..auth.auth import oauth2_scheme
from models.schemas.user_schemas import User
from sqlalchemy import Select
from models.models import User as UserOrm
from ..auth.jwt import decode_access_token, verify_password, get_password_hash


class UserStorage(BaseStorage):

    @classmethod
    async def retrieve_user(cls, query: Select) -> User:
        user_raw = await cls.db.fetch_row(query)
        if user_raw is None:
            raise HTTPException(status_code=400, detail="User not found error")
        return User.parse_obj(user_raw)

    @classmethod
    async def get_user_via_id(cls, user_id: int):
        sql = Select(UserOrm).where(UserOrm.id == user_id)
        return await cls.retrieve_user(sql)

    @classmethod
    async def get_user_via_email(cls, email: str):
        sql = Select(UserOrm).where(UserOrm.email == email)
        return await cls.retrieve_user(sql)

    @classmethod
    async def get_user_via_phone_number(cls, phone: str) -> User:
        sql = Select(UserOrm).where(UserOrm.phone == phone)
        return await cls.retrieve_user(sql)

    @classmethod
    async def login_user(cls, user: User, password: str) -> User:
        if verify_password(password, user.password):
            return user
        raise HTTPException(status_code=401, detail="Incorrect password")

    @classmethod
    async def get_current_user_via_token(cls, token: str = Depends(oauth2_scheme)) -> User:
        payload = decode_access_token(token)
        phone = payload.get('sub')
        if phone is None:
            raise HTTPException(status_code=400, detail="Phone is not defined")

        return await cls.get_user_via_phone_number(phone)
