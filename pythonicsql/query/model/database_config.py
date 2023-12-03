from dataclasses import dataclass
import ssl
from typing import TypedDict


@dataclass
class Config(TypedDict):
    uri: str
    min_size: int
    min_size: int
    ssl: bool


@dataclass
class DatabaseConfiguration(TypedDict):
    client: str
    config: Config
