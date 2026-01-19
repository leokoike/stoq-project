from src.domain.entities.pagination import Pagination
from src.domain.entities.product import Product
from src.domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    async def execute(
        self, page: int, size: int, filter_name: str = None
    ) -> Pagination[Product]:
        products = await self.product_repository.list_products(
            page=page, size=size, filter_name=filter_name
        )
        total_items = await self.product_repository.count_products(
            filter_name=filter_name
        )
        return Pagination[Product](
            page=page, size=size, total=total_items, items=products
        )
