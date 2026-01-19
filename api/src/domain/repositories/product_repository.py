from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID
from src.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    async def get_product_by_id(self, product_id: UUID) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def count_products(self, filter_name: str | None) -> int:
        raise NotImplementedError

    @abstractmethod
    async def list_products(
        self, page: int, size: int, filter_name: str | None
    ) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    async def create_product(self, product_data: Product) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def update_product(
        self, product_id: UUID, update_fields: dict[str, Any]
    ) -> None:
        raise NotImplementedError
