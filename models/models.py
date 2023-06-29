from sqlalchemy import String, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    vk_id: Mapped[int]
    is_admin: Mapped[bool]
    password: Mapped[str]


class UserAddress(Base):
    __tablename__ = "user_address"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(ForeignKey("user_address.address"))
    date: Mapped[datetime] = mapped_column(default=datetime.now)


class OrdersItems(Base):
    __tablename__ = "orders_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    item_size_color_id: Mapped[int] = mapped_column(ForeignKey("items_sizes_colors_availability.part_number"),
                                                    primary_key=True)


class Size(Base):
    __tablename__ = "sizes"

    rus_size: Mapped[int] = mapped_column(primary_key=True)


class Colors(Base):
    __tablename__ = "colors"

    name: Mapped[str] = mapped_column(String(50), primary_key=True)


class Categories(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(default=None)
    category_id: Mapped[int]


class ItemSizeColorAvailability(Base):
    __tablename__ = "items_sizes_colors_availability"

    part_number: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    size: Mapped[int] = mapped_column(ForeignKey("sizes.rus_size"))
    color: Mapped[str] = mapped_column(String(30), ForeignKey("colors.name"))
    price: Mapped[float] = mapped_column(default=0)
    is_available: Mapped[bool] = mapped_column(default=False)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), )


class UserHistory(Base):
    __tablename__ = 'user_history'
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime]
    url: Mapped[str] = mapped_column(default=None)
    user_agent: Mapped[str | None] = mapped_column(default=None)
