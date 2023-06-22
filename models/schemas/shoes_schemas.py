from pydantic import BaseModel


class Size(BaseModel):
    rus_size: int


class Color(BaseModel):
    name: str


class Category(BaseModel):
    id: int | None = None
    name: str


class Item(BaseModel):
    id: int | None = None
    name: str
    description: str
    category_id: int


class ItemsColorSizeAvailability(BaseModel):
    part_number: int
    item_id: int
    size: int
    color: str
    price: float
    is_available: bool
    images: list[str] = []


# Schemas

class ItemsListSchema(BaseModel):
    id: int
    name: str
    category: str


class ItemDetailSchema(BaseModel):
    item: Item
    options: list[ItemsColorSizeAvailability]

