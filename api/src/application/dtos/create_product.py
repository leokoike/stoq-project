from pydantic import BaseModel, Field

from src.domain.entities.product import EANType, SellingPlaceEnum


class CreateProductDTO(BaseModel):
    name: str = Field(..., max_length=150)
    ean: EANType
    price: float
    description: str = Field(..., max_length=250)
    active: bool
    selling_place: SellingPlaceEnum
    picture: bytes | None = None
