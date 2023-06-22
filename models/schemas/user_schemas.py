from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class User(BaseModel):
    id: int | None = None
    name: str
    phone: str
    email: EmailStr
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


class Order(BaseModel):
    id: int
    address: str
    data: datetime


class OrderItems(BaseModel):
    order_id: int
    item_size_color_id: int


class Size(BaseModel):
    rus_size: int


class Color(BaseModel):
    name: str


class ItemCreate(BaseModel):
    id: int
    name: str
    description: str


class ItemsColorSizeAvailability(BaseModel):
    part_number: int
    item_id: int
    size: int
    color: str
    price: float
    is_available: bool
