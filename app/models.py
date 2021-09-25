from enum import Enum

from pydantic import BaseModel


class Pokemon(BaseModel):
    name: str
    description: str
    habitat: str
    isLegendary: bool


class Dialect(Enum):
    SHAKESPEARE = 1
    YODA = 2
