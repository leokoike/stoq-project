from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, BeforeValidator, Field


class SellingPlaceEnum(Enum):
    EVENT = "event"
    STORE = "store"


def ean_validator(v: str | None) -> str:
    if v is None:
        return v
    if not (v.isnumeric() and len(v) == 13):
        raise ValueError("EAN must be a 13-digit numeric string")
    return v


EANType = Annotated[
    str,
    BeforeValidator(ean_validator),
]


class Product(BaseModel):
    id: UUID | None
    name: str = Field(..., max_length=150)
    ean: EANType
    inserted_at: datetime | None = None
    price: float
    description: str = Field(..., max_length=250)
    active: bool
    selling_place: SellingPlaceEnum
    picture: bytes | None
