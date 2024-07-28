from dataclasses import dataclass
from enum import Enum
from typing import NotRequired, Required, TypedDict


class DatabaseClientEnum(Enum):
    ASYNCPG = 1
    AIOSQLITE = 2


@dataclass
class Config(TypedDict):
    uri: NotRequired[str]
    host: NotRequired[str]
    port: NotRequired[int]
    user: NotRequired[str]
    database: NotRequired[str]
    password: NotRequired[str]
    timeout: NotRequired[float]
    ssl: NotRequired[bool]


@dataclass
class DatabaseConfiguration(TypedDict):
    dialect: Required[str]
    config: Required[Config]
    database_client_lib: NotRequired[DatabaseClientEnum]
