from . import models, schemas, utils

def get_user(user_id: int):
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str):
    return models.User.filter(models.User.email == email).first()


def get_users(skip: int = 0, limit: int = 100):
    return list(models.User.select().offset(skip).limit(limit))


def create_user(user: schemas.UserCreate):
    db_password = utils.set_password(user.password)
    db_user = models.User(name=user.name, phone=user.phone, email=user.email, password=db_password)
    db_user.save()
    return db_user

# ------------------------------------------

def get_order(order_id: int):
    return models.Order.filter(models.Order.id == order_id).first()


def get_orders(skip: int = 0, limit: int = 100):
    return list(models.Order.select().offset(skip).limit(limit))


def create_order(order: schemas.OrderCreate):
    db_order = models.User(address=order.address, date=order.date)
    db_order.save()
    return db_order

# ------------------------------------------

def get_size(size_rus_size: int):
    return models.Size.filter(models.Size.rus_size == size_rus_size).first()


def get_sizes(skip: int = 0, limit: int = 100):
    return list(models.Size.select().offset(skip).limit(limit))


def create_size(size: schemas.SizeCreate):
    db_size = models.size(rus_size=size.rus_size)
    db_size.save()
    return db_size

# ------------------------------------------

def get_color(color_name: str):
    return models.Color.filter(models.Color.name == color_name).first()


def get_colors(skip: int = 0, limit: int = 100):
    return list(models.Color.select().offset(skip).limit(limit))


def create_color(color: schemas.ColorCreate):
    db_color = models.Color(name=color.name)
    db_color.save()
    return db_color

# ------------------------------------------

def get_item(item_id: int):
    return models.Item.filter(models.Item.id == item_id).first()

def get_item_by_name(item_name: str):
    return models.User.filter(models.User.name == item_name).first()

def get_items(skip: int = 0, limit: int = 100):
    return list(models.Item.select().offset(skip).limit(limit))


def create_item(item: schemas.ItemCreate):
    db_item = models.Color(name=item.name, description=item.description)
    db_item.save()
    return db_item

# ------------------------------------------
