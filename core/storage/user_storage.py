from .base_storage import BaseStorage
from fastapi import Depends, HTTPException
from ..auth.oauth_scheme import oauth2_scheme
from models.schemas.user_schemas import User, UserRegisterSchema, UserRegisterVkSchema
from sqlalchemy import Select, Insert, Update, Delete
from sqlalchemy.sql.functions import count
from models.models import User as UserOrm
from ..auth.jwt import decode_access_token, verify_password, get_password_hash


class UserStorage(BaseStorage):

    @classmethod
    async def retrieve_user(cls, query: Select | Insert | Update | Delete) -> User:
        return await cls.retrieve_row(query, User, error_msg="User not found error")

    @classmethod
    async def check_unique_email(cls, email: str) -> int:
        sql = Select(count(UserOrm.email)).where(UserOrm.email == email)
        return await cls.db.fetch_val(sql)

    @classmethod
    async def check_unique_phone(cls, phone: str) -> int:
        sql = Select(count(UserOrm.phone)).where(UserOrm.phone == phone)
        return await cls.db.fetch_val(sql)

    @classmethod
    async def create_user(cls, user: UserRegisterSchema) -> User:
        if await cls.check_unique_email(user.email) != 0 or await cls.check_unique_phone(user.phone) != 0:
            raise HTTPException(status_code=422, detail="Not unique phone or email")
        user.password = get_password_hash(user.password)
        sql = Insert(UserOrm).values(**user.dict(exclude_none=True)).returning(UserOrm)
        return await cls.retrieve_user(sql)

    @classmethod
    async def get_or_create_user_via_vk(cls, user: UserRegisterVkSchema) -> User:
        sql = Select(count(UserOrm)).where(UserOrm.vk_id == user.vk_id)
        if await cls.db.fetch_val(sql) == 0:
            sql = Insert(UserOrm).values(**user.dict()).returning(UserOrm)
            return await cls.retrieve_user(sql)

        return await cls.get_user_via_vk_id(user.vk_id)

    @classmethod
    async def get_user_via_vk_id(cls, vk_id: int) -> User:
        sql = Select(UserOrm).where(UserOrm.vk_id == vk_id)
        return await cls.retrieve_user(sql)

    @classmethod
    async def get_user_via_id(cls, user_id: int) -> User:
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
        sub = payload.get('sub')
        auth_type = payload.get('authType')

        if sub is None or auth_type is None:
            raise HTTPException(status_code=400, detail="Subject or authType is not defined")

        if auth_type == 'website':
            return await cls.get_user_via_phone_number(sub)
        if auth_type == 'vk':
            return await cls.get_user_via_vk_id(sub)
