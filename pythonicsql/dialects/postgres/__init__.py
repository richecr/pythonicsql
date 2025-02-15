from typing import Generic, List, TypeVar

import asyncpg

from pythonicsql.dialects.client import Client
from pythonicsql.query.model.database_config import Config


class PostgresSQL(Client):
    __slots__ = ["dialect", "db", "connection"]

    def __init__(self, dialect: str, config: Config) -> None:
        super().__init__(dialect, config)

    async def connect(self) -> None:
        uri = self.config.get("uri")
        if uri:
            self.db = await asyncpg.create_pool(dsn=uri)
            return

        self.db = await asyncpg.create_pool(
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
            port=self.config["port"],
            host=self.config["host"],
            timeout=self.config["timeout"],
            ssl=self.config["ssl"],
        )

    async def close(self) -> None:
        if self.db is None:
            return

        await self.db.close()

    async def execute(self, sql: str) -> str:
        if self.db is None:
            raise Exception("Database connection is not established")

        return await self.db.execute(sql)

    async def fetch(self, sql: str) -> List[asyncpg.Record]:
        if self.db is None:
            raise Exception("Database connection is not established")

        async with self.db.acquire() as connection:
            return await connection.fetch(sql)

    async def fetch_one(self, sql: str) -> asyncpg.Record | None:
        if self.db is None:
            raise Exception("Database connection is not established")

        async with self.db.acquire() as connection:
            return await connection.fetchrow(sql)
