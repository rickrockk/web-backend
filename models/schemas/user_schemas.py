from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class User(BaseModel):
    id: int | None = None
    name: str
    phone: str
    email: EmailStr
    is_admin: bool
    vk_id: int | None = None
    password: str


class UserRegisterSchema(BaseModel):
    name: str
    phone: str
    email: str
    password: str


class UserAddress(BaseModel):
    id: int
    user_id: int
    address: str

