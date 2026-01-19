from pydantic import BaseModel, Field

from src.domain.entities.product import EANType, SellingPlaceEnum


class UpdateProductDTO(BaseModel):
    name: str | None = Field(None, max_length=150)
    ean: EANType | None = None
    price: float | None = None
    description: str | None = Field(None, max_length=250)
    active: bool | None = None
    selling_place: SellingPlaceEnum | None = None
    picture: bytes | None = None
