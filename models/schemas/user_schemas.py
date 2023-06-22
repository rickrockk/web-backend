from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class User(BaseModel):
    id: int | None = None
    name: str
    phone: str | None = None
    email: EmailStr | None = None
    is_admin: bool
    vk_id: int | None = None
    password: str | None = None


class UserRegisterSchema(BaseModel):
    name: str
    phone: str
    email: str
    password: str


class UserRegisterVkSchema(BaseModel):
    name: str
    email: str
    vk_id: int


class UserAddress(BaseModel):
    id: int
    user_id: int
    address: str

