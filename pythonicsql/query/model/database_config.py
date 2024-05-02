from dataclasses import dataclass
from typing import NotRequired, TypedDict


@dataclass
class Config(TypedDict):
    uri: str
    min_size: NotRequired[int]
    max_size: NotRequired[int]
    ssl: NotRequired[bool]


@dataclass
class DatabaseConfiguration(TypedDict):
    dialect: str
