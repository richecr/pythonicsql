from dataclasses import dataclass


@dataclass
class Raw:
    def __init__(self, sql: str):
        self.sql = sql
