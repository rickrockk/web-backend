from database import database


class BaseStorage:
    def __init__(self):
        self.db = database

