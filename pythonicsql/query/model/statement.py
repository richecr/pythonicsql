from typing import Any

from pydantic import BaseModel


class Statements(BaseModel):
    type: str
    value: Any
    grouping: str
    column: str = ""
    condition: str = " and"
