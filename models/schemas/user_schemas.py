from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    password: str

class UserAddressCreate(BaseModel):
    id: int
    user_id: int
    address: str

class OrderCreate(BaseModel):
    id: int
    address: str
    data: datetime

class OrderItemsCreate(BaseModel):
    order_id: int
    item_size_color_id: int

class SizeCreate(BaseModel): 
    rus_size: int

class ColorCreate(BaseModel):
    name: str(30)

class ItemCreate(BaseModel):
    id: int
    name: str(50)
    description: str

class ItemsColorSizeAvailabilityCreate(BaseModel): 
    part_number: int
    item_id: int
    size: int
    color: str
    price: float
    is_available: bool