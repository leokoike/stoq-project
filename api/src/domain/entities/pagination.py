from pydantic import BaseModel


class Pagination[T](BaseModel):
    page: int
    size: int
    total: int
    items: list[T]
