import asyncpg
from sqlalchemy import Select, Insert, Delete, Update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects import postgresql
from config import Config
from loguru import logger


class Base(DeclarativeBase):
    pass


class Database:
    __instance: 'Database' = None
    __connection: asyncpg.connection.Connection | None = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def check_connection(self):
        if self.__connection is None:
            raise ConnectionError("Database is not connected.")

    async def connect(self):
        if self.__connection is None:
            self.__connection = await asyncpg.connect(Config.postgres_url)
        return self.__connection

    async def execute(self, query: Select | Insert | Delete | Update):
        self.check_connection()
        return await self.__connection.execute(
            str(query.compile(compile_kwargs={"literal_binds": True}, dialect=postgresql.dialect())))

    async def fetch(self, query: Select | Insert | Delete | Update):
        self.check_connection()
        return await self.__connection.fetch(
            str(query.compile(compile_kwargs={"literal_binds": True}, dialect=postgresql.dialect())))

    async def fetch_val(self, query: Select | Insert | Delete | Update):
        self.check_connection()
        return await self.__connection.fetchval(
            str(query.compile(compile_kwargs={"literal_binds": True}, dialect=postgresql.dialect())))

    async def fetch_row(self, query: Select | Insert | Delete | Update):
        self.check_connection()
        return await self.__connection.fetchrow(
            str(query.compile(compile_kwargs={"literal_binds": True}, dialect=postgresql.dialect())))


database = Database()


async def connect_database():
    try:
        await database.connect()
        logger.info("Database connected")

    except Exception as exc:
        logger.error("DB Not connected. {_type} : {exc}", _type=str(type(exc)), exc=str(exc))
