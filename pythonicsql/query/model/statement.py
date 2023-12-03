from dataclasses import dataclass
from typing import Any


@dataclass
class Statements:
    type: str
    value: Any
    grouping: str
    column: str = ""
    condition: str = " and"
    operator: str = "="
