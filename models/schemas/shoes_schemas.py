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


class OptionSchema(BaseModel):
    part_number: int
    item_id: int | None = None
    size: int
    color: str
    price: float
    is_available: bool
    images: list[str] | None = None


# Schemas

class ItemCreateSchema(BaseModel):
    name: str
    description: str
    category_id: int


class OptionCreateSchema(BaseModel):
    part_number: int
    size: int
    color: str
    price: float
    is_available: bool
    images: list[str] | None = None


class ItemsListSchema(BaseModel):
    id: int
    name: str
    category: str


class ItemOptionCreateSchema(BaseModel):
    item: ItemCreateSchema
    options: list[OptionCreateSchema]

# class MailCreate(BaseModel):
#     me: str
#     to: str
#     text: str
#     subject: str


class ItemDetailSchema(BaseModel):
    item: Item
    options: list[OptionSchema]


class CreateCategorySchema(BaseModel):
    name: str
