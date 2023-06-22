from .base_storage import BaseStorage
from fastapi import Depends, HTTPException
from ..auth.oauth_scheme import oauth2_scheme
from models.schemas.user_schemas import User, UserRegisterSchema
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
